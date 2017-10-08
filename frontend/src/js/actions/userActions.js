import axios from 'axios';

export function login(user) {
  return function(dispatch){
    axios.post('http://localhost:8000/backend/login/',{
        user
    })
    .then((response)=>{
        if(response.data.message==='success'){
          console.log(response);
          localStorage.setItem('cookie', JSON.stringify(response.data.cookie));
            dispatch( {
              type: 'SET_USER',
              payload:response.data,
            })
        }
    })
    .catch((err)=>{
      console.log(err);
    });
    axios.get('http://localhost:8000/backend/get_top_games/?n=100')
        .then((res2)=>{
          dispatch({
            type: 'SET_DISCOVER',
            payload:res2.data,
          })
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

export function getGameInfo(gameID,username){
  const url='http://localhost:8000/backend/get_game_info/?gameid='+gameID+'&username='+username;
  return axios.get(url);
}

export function signup(user){
  console.log(user);
  return function(dispatch){
    axios.post('http://localhost:8000/backend/register/',{
        user
    })
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


export function getReccomendation1(username){
  const url='http://localhost:8000/backend/recommendation_v1/?username='+username;
  return axios.get(url);
}


export function Verification(key){
  const url='http://localhost:8000/backend/activate/'+key;
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
