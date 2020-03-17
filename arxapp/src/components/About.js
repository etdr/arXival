import React from 'react';

import './About.scss';

const About = (props) => {


  return (
    <div id="about-div">
      <h2>About arXival</h2>

      <p>This was a project for <a href="https://www.thisismetis.com/" target="_blank">Metis</a>'s Chicago winter 2020 cohort.</p>

      <p>
        For a previous project, I experimented with Latent Dirichlet Allocation, fastText, and word2vec using arXiv papers from the first half of 2019. Now, for this project, I tightened my focus and concentrated on creating a paper recommender system using document similarity measures.
      </p>

      <p>
        The repo is available at ...
      </p>
    </div>
  )
}

export default About;