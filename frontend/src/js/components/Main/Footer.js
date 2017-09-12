import React from "react";

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
export default class foot extends React.Component {
  render() {
    return(
	    <div>
	    <footer>
	      SteamR ©2017 Created by a fucking team
	    </footer>
	    </div>
    );
  }
}

