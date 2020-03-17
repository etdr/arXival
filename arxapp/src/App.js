import React from 'react';
import './App.scss';

import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

import Navbar from './components/Navbar';
import Recommender from './components/Recommender';
import About from './components/About';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Switch>
          <Route path="/rec">
            <Recommender />
          </Route>
          <Route path="/about">
            <About />
          </Route>
        </Switch>
        <div id="spacer">
        </div>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
