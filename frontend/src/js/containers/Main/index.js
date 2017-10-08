import React from "react";
// import { connect } from "react-redux";
import { Link, Switch, Route, Redirect } from 'react-router-dom';
import Nav from "./Nav";
import Search from "../../containers/Search";
import Discover from "../../containers/Discover";
import Profile from "../../containers/Profile";
import Results from "../Results";
import SubResult from "../Results/SubResult.js";
import Activate from "./Activate.js";


export default class Main extends React.Component {
  render() {
    return(
      <div >
        <Nav path={this.props.location.pathname}/>
        <div className='content'>
            <Switch>
                <Route exact path='/' render={() => <Redirect to='/discover'/>} />
                <Route path='/discover' component={Discover} />
                <Route path='/search' component={Search} />
                <Route path='/profile' component={Profile} />
                <Route path='/results' component={Results} />
                <Route path='/games/:gameID' component={SubResult} />
                <Route path='/activate/:key' component={Activate} />
            </Switch>
        </div>
      </div>
    );
  }
}
