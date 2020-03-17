import React from 'react';
import {Link} from 'react-router-dom';

import './Navbar.scss';



const Navbar = props => {







  return (
    <div id="nav-div">
      <h1>arXival</h1>
      <nav>
        <ul>
          <li><Link to="/rec">arXapp</Link></li>
          <li><Link to="/about">about</Link></li>
          <li>the arXival repo</li>
        </ul>
      </nav>
    </div>
  );
}

export default Navbar;