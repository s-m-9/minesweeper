import React, { Component, Fragment } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Game from './Game'
import './App.css';

/**
 * Browser Paths
 */

class App extends Component {

    render() {
        // console.log(this.state.boardData)
        return (
            <BrowserRouter basename={process.env.PUBLIC_URL}>
                <Switch>
                    <Route exact path="/" component={Game} />
                    <Route path="/:id" component={Game} />
                </Switch>
            </BrowserRouter>
        );
    }
}


export default App;
