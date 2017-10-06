import axios from 'axios';

export function login(user) {
  return function(dispatch){
    axios.post('http://localhost:8000/backend/login/',{
        user
    })
    .then((response)=>{
        console.log(response.data);
        if(response.data.message==='success'){
          localStorage.setItem('cookie', JSON.stringify(response.data.cookie));
            dispatch( {
              type: 'SET_USER',
              payload:response.data.user,
            })
        }
    })
    .catch((err)=>{
      console.log(err);
    })
    }
}

export function logout(){
  return {
    type: 'DELETE_USER',
  }
}

export function searchGame(keyword,isFetched){
    console.log("hehe");
    const url='http://localhost:8000/backend/search_game/?q='+ keyword + "&category=";
    return function(dispatch){
    axios.get(url)
        .then((res)=>{
          console.log("research result",res);
          dispatch( {
            type: 'FETCH_RESULT',
            payload:res.data,
          })
          isFetched();
        });
    }
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


export function signup(user){
  console.log(user);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/register/',{
        user
    })
    .then((response)=>{
        console.log(response.data);
        if(response.data.message==='success'){
            dispatch( {
              type: 'SET_USER',
              payload:response.data.user,
            })
        }
    })
    .catch((err)=>{
      console.log(err);
    })
    }
}

export function getProfile(username){
  console.log("get profile run");
  const url = 'http://localhost:8000/backend/user_prof/username='+ username ;
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
