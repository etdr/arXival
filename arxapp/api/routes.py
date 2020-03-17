from ..api import app

from flask import request

from ...code import doc_sim as ds
from ..api import fetch_info as fi

@app.route('/')
@app.route('/index')
def index():
    return {"testing": 3}



@app.route('/aID', methods=['POST'])
def process_aid_ds():
    aID = request.get_json()['aID']
    doc_str = ds.get_doc_str(aID, field='text_dtr')


    doc_results = ds.cssim_rank(doc_str)
    for dr in doc_results:
        dr['title'] = fi.fetch_title(dr['aID'])

    return doc_results
