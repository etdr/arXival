import React, {useState} from 'react';

import RecResults from './RecResults';

const BASEURL = 'http://35.196.48.219:5000'

const Recommender = (props) => {




  const [excerpt, setExcerpt] = useState("");

  const [results, setResults] = useState([]);


  

  function fetchResultsforaID (aID) {
    setResults([]);
    fetch(BASEURL+'/aID', {
      method: 'POST',
      body: {
        'aID': aID
      }
    }).then(r => r.json())
      .then(rjs => {
        let rs = [];
        for (let p of rjs.doc_results) {
          rs.push(p);
        }
        setResults(rs);
      })
  }



  return (
    <div id="rec-div">
      <div id="input-div">
        <h3>Enter an arXiv ID:</h3>
        <input /> <button onClick={fetchResultsforaID('1901.08000')}>go</button>
        <h3>Or invent some text:</h3>
        <textarea></textarea> <button>go</button>
        <h3>Or press here to generate text</h3>
        <button>generate</button>
        <button>go</button>
        </div>
      <RecResults results={results} />
    </div>
  );


}

export default Recommender;