

import os
import tarfile
import gzip
import re
from pymongo import MongoClient
from subprocess import run

client = MongoClient()
db = client.arXiv


def extract_all_to_dirs(delete_archive=True):
    for gzfile in (f for f in os.listdir() if os.path.splitext(f)[1] == '.gz'):
        extract_to_dir(gzfile, delete_archive=delete_archive)



def extract_to_dir(gzfile, delete_archive=True):
    path = os.path.splitext(gzfile)[0]
    os.mkdir(path)
    try:
        t = tarfile.open(gzfile)
        texs = [f for f in t.getmembers() if '.tex' == f.name[-4:]]
        for tex in texs:
            t.extract(tex, path)
        t.close()
    except tarfile.ReadError:
        with open(path+'/'+path+'.tex', 'wb') as f:
            with gzip.open(gzfile, 'rb') as g:
                f.write(g.read())
    if delete_archive:
        os.remove(gzfile)





def extract_text_from_all(cstr):
    coll = db[cstr]

    dirs = [d for d in os.listdir() if os.path.isdir(d)]

    for d in dirs:
        extract_text_from_texs(d, coll)

    


def extract_text_from_texs(aID, coll):
    texfiles = [f for f in os.listdir(aID) if os.path.isfile(aID+'/'+f)]
    texs = dict()
    for texfile in texfiles:
        try:
            with open(aID+'/'+texfile, 'rt') as f:
                print('trying',aID+'/'+texfile)
                texs[os.path.splitext(texfile)[0]] = f.read()
        except UnicodeDecodeError:
            with open(aID+'/'+texfile, 'rt', encoding='latin-1') as f:
                print('trying',aID+'/'+texfile)
                texs[os.path.splitext(texfile)[0]] = f.read()
        except UnicodeDecodeError:
            return
                
    
    primdocs = list(filter(lambda d: '\\begin{document}' in d, texs.values()))
    try: 
        primdoc = primdocs[0]
    except IndexError:
        return

    os.chdir(aID)
    try:
        proc = run(['detex', '-r'], input=primdoc, text=True, capture_output=True)
    except UnicodeDecodeError:
        os.chdir('..')
        return
    output = proc.stdout

    output = output.replace('\n', ' ')
    output = output.replace('noun verbs noun', '__MATH1__')
    output = output.replace('noun', '__MATH0__')

    






    os.chdir('..')

    #tex, abstract = document_process(primdoc, texs)

    # add tex and abstract to mongo
    coll.update_one({'aID': aID}, {'$set': {'text_dtr': output}})







def document_process(tex, texs):
    # remove comments
    tex = re.sub(r'^%.*?$', ' ', tex, flags=re.M)
    # remove \\ at end of line
    # replace newlines with spaces
    tex = re.sub(r'\n', ' ', tex)

    # extract abstract
    abstract = None
    if '\\begin{abstract}' in tex:
        abstract = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', tex).group(1)
    if '\\abstract' in tex:
        abstract = re.search(r'\\abstract{(.*?[^\\])}', tex).group(1)

    # remove everything but document
    tex = re.sub(r'.*?\\begin{document}', '', tex)
    tex = re.sub(r'\\end{document}.*', '', tex)


    # input and include
    split_filter = filter(lambda x: x is not None, re.split(r'(\\input{.*?})|(\\include{.*?})', tex))
    split_list = []
    for t in split_filter:
        if (m := re.match(r'\\input{(.*)}', t)):
            split_list.append(texs[m.group(1)])
        elif (m := re.match(r'\\include{(.*)}', t)):
            split_list.append(texs[m.group(1)])
        else:
            split_list.append(t)
    tex = ' '.join(split_list)


    # actually process abstract and document
    abstract = regex_process(abstract)
    tex = regex_process(tex)

    return (tex, abstract)



LATEX_STRIP = ['section', 'subsection', 'subsubsection', 'paragraph',
    'emph', 'em', 'textbf']
LATEX_STRIP_ENV = ['proof', 'theorem', 'corollary', 'lemma', 'proposition', 'algorithm', 'assumption',
    'itemize',
]

# delete is default so we don't need to catch all of these
LATEX_DELETE = ['label', 'ref', 'eqref', 'abstract']
LATEX_DELETE_ENV = ['table', 'figure', 'abstract', 'align']

LATEX_TOKEN = ['cite', 'citep', 'citet']
LATEX_TOKEN_ENV = ['equation']

LATEX_BIB = ['thebibliography']


def regex_process(tex):
    # bib removal
    tex = re.sub(r'\\begin{thebibliography}.*\\end{thebibliography}(?:{.*?})*', ' ', tex)


    #math replacement
    tex = re.sub(r'\$\$.*?\$\$', '__MATH__', tex)
    tex = re.sub(r'\$.*?\$', '__MATH__', tex)



    # Strips
    strips_redict = {c: re.compile(r'\\'+c+r'\*?(?:\[.*?\])*{(.*?)}') for c in LATEX_STRIP}
    for strip_re in strips_redict.values():
        tex = strip_re.sub(r'\1', tex)

    strips_encl_redict = {c: re.compile(r'{\\'+c+r'\*?\s(.*?)[^\\]}') for c in LATEX_STRIP+LATEX_STRIP_ENV}
    for strip_encl_re in strips_encl_redict.values():
        tex = strip_encl_re.sub(r'\1', tex)


    strips_env_redict = {c: re.compile(r'\\begin{'+c+r'\*?}(.*?)\\end{'+c+'}') for c in LATEX_STRIP_ENV}
    for strip_env_re in strips_env_redict.values():
        tex = strip_env_re.sub(r'\1', tex)

    #beginre = re.compile(r'\\begin{([a-zA-Z]+)}(.*?)\\end{\1}')
    #while beginre.findall(tex):
    #    tex = beginre.sub(r'\_\_\1\_\_'.upper(), tex)





    # Deletes
    delete_redict = {c: re.compile(r'\\'+c+r'{.*?}') for c in LATEX_DELETE}
    for del_re in delete_redict.values():
        tex = del_re.sub(' ', tex)

    delete_env_redict = {c: re.compile(r'\\begin{'+c+r'}(.*?)\\end{'+c+'}') for c in LATEX_DELETE_ENV}
    for del_env_re in delete_env_redict.values():
        tex = del_env_re.sub(' ', tex)



    #tex = re.sub(r'\\cite{.*?}', '__CITE__', tex)  
    #tex = re.sub(r'\\citep{.*?}', '__CITE__', tex)

    # Tokens
    token_redict = {c: {'token': '__'+c.upper()+'__', 're': re.compile(r'\\'+c+r'{.*?}')} for c in LATEX_TOKEN}
    for d in token_redict.values():
        tex = d['re'].sub(d['token'], tex)


    token_env_redict = {}

    
    # all other backslash commands
    tex = re.sub(r'\\[a-zA-Z]+\*?(?:\[.*?\])*(?:{.*?})*', ' ', tex)


    # all other backslash envs
    tex = re.sub(r'\\begin{([a-zA-Z]+\*?)}(.*?)\\end{\1}', ' ', tex)


    # tilde removal
    tex = re.sub(r'([^\\])\~', r'\1', tex)
    # backslash char replacement
    tex = re.sub(r'\\(\s)', r'\1', tex)



    return tex