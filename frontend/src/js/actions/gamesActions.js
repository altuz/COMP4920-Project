import axios from "axios";




export function add_to_game_list(username,gameID){
  var user={
    username : username,
    gameid : gameID,
    played : true,
    wish : false,
  }
  console.log(user);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/edit_list/',{
      user
    }).then((res=>{
      console.log(res);
      dispatch( {
        type: 'UPDATE_GAMELIST',
        payload:res.data.gamelist,
      })
    }))
  }

}

export function add_to_wish_list(username,gameID){
  var user={
    username : username,
    gameid : gameID,
    played : false,
    wish : true,
  }
  console.log(user);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/edit_list/',{
      user
    }).then((res=>{
      console.log(res);
    }))
  }
}
// export function fetchTweets() {
//   return function(dispatch) {
//     dispatch({type: "FETCH_TWEETS"});
//
//     /*
//       http://rest.learncode.academy is a public test server, so another user's experimentation can break your tests
//       If you get console errors due to bad data:
//       - change "reacttest" below to any other username
//       - post some tweets to http://rest.learncode.academy/api/yourusername/tweets
//     */
//     axios.get("http://rest.learncode.academy/api/reacttest/tweets")
//       .then((response) => {
//         dispatch({type: "FETCH_TWEETS_FULFILLED", payload: response.data})
//       })
//       .catch((err) => {
//         dispatch({type: "FETCH_TWEETS_REJECTED", payload: err})
//       })
//   }
// }

