import React from "react";
// import { connect } from "react-redux";
import { Link, Switch, Route, Redirect } from 'react-router-dom';
import Nav from "./Nav";
import Footer from "./Footer";


// @connect((store) => {
//   return {
//     user: store.user.user,
//     userFetched: store.user.fetched,
//     tweets: store.tweets.tweets,
//   };
// })
export default class Main extends React.Component {
  render() {
    return(
      <div >
        <Nav />
      </div>
    );
  }
}
