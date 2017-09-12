import React from "react";
import {
 	Navbar,
 	FormGroup,FormControl,
 	Button,
 	Nav,
 	NavItem,
 	NavDropdown,
 	MenuItem } from 'react-bootstrap';
// import { connect } from "react-redux";

// import { fetchUser } from "../actions/userActions"
// import { fetchTweets } from "../actions/tweetsActions"

// @connect((store) => {
//   return {
//     user: store.user.user,
//     userFetched: store.user.fetched,
//     tweets: store.tweets.tweets,
//   };
// })
export default class Navi extends React.Component {
  render() {
    return(
  <Navbar>
    <Navbar.Header>
      <Navbar.Brand>
        <a href="#">SteamR</a>
      </Navbar.Brand>
    </Navbar.Header>
    <Nav>
      <NavItem eventKey={1} href="#">Porn</NavItem>
      <NavItem eventKey={2} href="#">Wanking</NavItem>
      <NavDropdown eventKey={3} title="FuckMe" id="basic-nav-dropdown">
        <MenuItem eventKey={3.1}>Action</MenuItem>
        <MenuItem eventKey={3.2}>Another action</MenuItem>
        <MenuItem eventKey={3.3}>Something else here</MenuItem>
        <MenuItem divider />
        <MenuItem eventKey={3.4}>Separated link</MenuItem>
      </NavDropdown>
    </Nav>
  </Navbar>
    );
  }
}

