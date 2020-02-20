
from pymongo import MongoClient
import subprocess
import os
import os.path as path
import re
from datetime import datetime
import xml.etree.ElementTree as ET
import requests



client = MongoClient()


db = client.arXiv





def insert_month(month):
    c = db[month]
    for root, dirs, files in os.walk('../arxiv/s3/'+month):
        #files = list(files)
        for f in files:
            fn, ext = path.splitext(f)
            if 'layout' in fn:
                continue
            with open('../arxiv/s3/'+month+'/'+f, 'rt') as f0:
                text = f0.read()
            try:
                with open('../arxiv/s3/'+month+'/'+fn+'_layout.txt', 'rt') as f1:
                    text_layout = f1.read()
            except:
                text_layout = None
            subject, date = extract_info(text)
            c.insert_one({
                'aID': fn,
                'subject': subject,
                'date': date,
                'text': text,
                'text_l': text_layout,
            })
            print('inserted',fn)





def insert_document():
    pass


def extract_info(doc):
    r = re.search('arXiv:.*\[(?P<field>.*)\]\s(?P<date>.*)$', doc, re.M)
    if r:
        try:
            dt = datetime.strptime(r.group('date'), '%d %b %Y')
        except ValueError:
            dt = None
        return r.group('field'), dt
    else:
        return (None, None)

META_URL = 'http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:'
META_SUFFIX = '&metadataPrefix=arXiv'

def supplement_info(month):
    c = db[month]
    for doc in c.find():
        for i in range(10):
            try:
                if 'subjects' not in doc.keys():
                    r = requests.get(META_URL+doc['aID']+META_SUFFIX)
                    root = ET.fromstring(r.content)
                    cats = root.find('.//{http://arxiv.org/OAI/arXiv/}categories').text.split(' ')
                    date = datetime.strptime(root.find('.//{http://arxiv.org/OAI/arXiv/}created').text, '%Y-%m-%d')
                    c.update_one({'aID':doc['aID']}, {'$set':{'subjects':cats, 'date2':date}})
                    print('updated',doc['aID'],'with',cats,date)
                else:
                    print('skipped',doc['aID'])
            except:
                continue
            else:
                break
