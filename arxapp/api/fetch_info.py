
import requests
import xml.etree.ElementTree as ET
import re


META_URL = 'http://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:'
META_SUFFIX = '&metadataPrefix=arXiv'



def fetch_title(aID):
    r = requests.get(META_URL+aID+META_SUFFIX)
    root = ET.fromstring(r.content)
    title = re.sub(r'\s+', ' ', root.find('.//{http://arxiv.org/OAI/arXiv/}title').text)
    return title