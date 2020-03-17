import React, {useState} from 'react';

import RecResults from './RecResults';

const Recommender = (props) => {




  const [excerpt, setExcerpt] = useState("");








  return (
    <div id="rec-div">
      <div id="input-div">
        <h3>Enter an arXiv ID:</h3>
        <input />
        <h3>Or invent some text:</h3>
        <textarea></textarea>
        <h3>Or press here to generate text</h3>
        <button>generate</button>
        <button>GO</button>
        </div>
      <RecResults />
    </div>
  );


}

export default Recommender;