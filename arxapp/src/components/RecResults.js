import React from 'react';






const RecResults = (props) => {


  return (
    <div id="rec-results-div">
      <ul>
        {props.results.map(r => {
          <li>
            <h3>{r.title}</h3>
            <p>Date: {r.date}</p>
            <p>Subjects:</p>
            <ul>
              {r.subjects.map(s => <li>{s}</li>)}
            </ul>
          </li>
        })}
      </ul>
    </div>
  )
}

export default RecResults;