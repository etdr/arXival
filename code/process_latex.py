

import os
import tarfile
import re



def extract_all_to_dirs(delete_archive=True):
    for gzfile in (f for f in os.listdir() if os.path.splitext(f)[1] == '.gz'):
        extract_to_dir(gzfile, delete_archive=delete_archive)



def extract_to_dir(gzfile, delete_archive=True):
    path = os.path.splitext(gzfile)[0]
    os.mkdir(path)
    t = tarfile.open(gzfile)
    texs = [f for f in t.getmembers() if '.tex' == f.name[-4:]]
    for tex in texs:
        t.extract(tex, path)
    t.close()
    if delete_archive:
        os.remove(gzfile)







def extract_text_from_texs(aID):
    texfiles = os.listdir(aID)
    texs = dict()
    for texfile in texfiles:
        with open(aID+'/'+texfile, 'rt') as f:
            texs[os.path.splitext(texfile)[0]] = f.read()
    
    primdocs = list(filter(lambda d: '\\documentclass' in d, texs))
    try: 
        len(primdocs) > 1
        
    except:
        raise
    primdoc = primdocs[0]




def regex_process(tex):
    tex = re.sub(r'^%.*?$', ' ', tex, flags=re.M)
    tex = re.sub(r'\n', ' ', tex)


    # bib removal
    tex = re.sub(r'\\begin{thebibliography}.*\\end{thebibliography}', ' ', tex)


    #math replacement
    tex = re.sub(r'\$.*?\$', '__MATH__', tex)

    tex = re.sub(r'\\cite{.*?}', '__CITE__', tex)  
    tex = re.sub(r'\\citep{.*?}', '__CITE__', tex)
    
    beginre = re.compile(r'\\begin{([a-z][a-zA-Z]*)}(.*?)\\end{\1}')
    while beginre.findall(tex):
        tex = beginre.sub(r'\_\_\1\_\_'.upper(), tex)

    return tex