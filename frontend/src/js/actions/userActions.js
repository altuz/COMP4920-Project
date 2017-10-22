import axios from 'axios';

export function login(user,isFail) {
  return function(dispatch){
    axios.post('http://localhost:8000/backend/login/',{
        user
    })
    .then((response)=>{
        if(response.data.message ==='success'){
          console.log(response.data);
          localStorage.setItem('cookie', JSON.stringify(response.data.cookie));
            dispatch( {
              type: 'SET_USER',
              payload:response.data,
            })
        } else {
            isFail();
        }
    })
    .catch((err)=>{
      console.log('fdfdfdf')
      isFail();
      console.log(err);
    });
    }
}

export function logout(){
  return {
    type: 'DELETE_USER',
  }
}

export function searchGame(isFetched,state){
    const keyword = {
      q:state.q,
      genre:state.selected_genre,
      category: state.selected_category,
    }

    const url='http://localhost:8000/backend/search_game/?q='+ state.q + "&category="+state.selected_category
        + "&genre="+state.selected_genre;
    return function(dispatch){
      dispatch({
        type: "SEARCHING_GAME",
        payload:keyword
      });

      axios.get(url)
        .then((res)=>{
          dispatch( {
            type: 'FETCH_RESULT',
            payload:res.data,
          })
          isFetched();
        })
    }
}

export function edit_hrs(game_id,user,hours){
  const url = 'http://localhost:8000/backend/edit_game_hrs/';
  const edit_game_hrs ={
    username :user.user_name,
    gameid: game_id,
    played_hrs: hours,
  }
  return axios.post(url, {
    edit_game_hrs
  })
}

export function clearResult(){
  return function(dispatch){
    dispatch( {
      type:'CLEAR_RESULT',
    })
  }
}

export function getDiscover() {
  const url='http://localhost:8000/backend/get_top_games/?n=100';
  return axios.get(url);
}

export function getGameInfo(gameID,username){
  const url='http://localhost:8000/backend/get_game_info/?gameid='+gameID+'&username='+username;
  return axios.get(url);
}

export function signup(user,isFail){
  console.log(user);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/register/',{
        user
    })
    .then((response)=>{
        if(response.data ==='register created successfully'){

        } else {
            isFail();
        }
    })
    .catch((err)=>{
      console.log('fdfdfdf')
      isFail();
      console.log(err);
    });
    }
}


export function edit_profile(edit){
  console.log(edit);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/edit_profile/',{
        edit
    })
    }
}


export function getRecommendation1(username){
  const url='http://localhost:8000/backend/recommend_v1/?username='+username;
  return axios.get(url);
}


export function Verification(key){
  const url='http://localhost:8000/backend/activate/'+key;
  return axios.get(url);
}

export function getRecommendation2(username){
    const url='http://localhost:8000/backend/recommend_v2/?username='+username;
    return axios.get(url);
}

 export function getFollowList(username){
    const url='http://localhost:8000/backend/follow_list/?username='+username;
    return axios.get(url);
}

export function getProfile(username){
    const url='http://localhost:8000/backend/user_prof/?username='+username;
    return axios.get(url);
}

export function isFollow(user1,user2){
    const url='http://localhost:8000/backend/is_following/?user1='+user1+'&user2='+user2;
    return axios.get(url);
}

export function follow(user){
    return function(dispatch){
    axios.post('http://localhost:8000/backend/follow_user/',{
        user
    })
    .catch((err)=>{
      console.log(err);
    });
    }
}

export function unfollow(user){
    return function(dispatch){
    axios.post('http://localhost:8000/backend/unfollow_user/',{
        user
    })
    .catch((err)=>{
      console.log(err);
    });
    }
}

export function search_user(q){
    const url='http://localhost:8000/backend/search_user/?q='+q;
    return axios.get(url);
}


export function updatepprofile(username){
    const url ='http://localhost:8000/backend/get_game_list/?username='+username;
    return axios.get(url);
}






// export function setUserName(name) {
//   return {
//     type: 'SET_USER_NAME',
//     payload: name,
//   }
// }
//
// export function usersignup() {
//   return {
//     type: 'SET_USER_AGE',
//     payload: age,
//   }
// }
