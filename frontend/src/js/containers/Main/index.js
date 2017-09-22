import React from "react";
// import { connect } from "react-redux";
import { Link, Switch, Route, Redirect } from 'react-router-dom';
import Nav from "./Nav";
import Search from "../../containers/Search";
import Discover from "../../containers/Discover";


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
            </Switch>
        </div>
      </div>
    );
  }
}
