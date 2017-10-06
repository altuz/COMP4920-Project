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

export function searchGame(keyword){
    console.log("hehe");
    const url='http://localhost:8000/backend/search_game/?q='+ keyword + "&category=";
    return axios.get(url);
}

export function clearResult(){
  return function(dispatch){
    dispatch( {
      type:'CLEAR_RESULT',
    })
  }
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
// return function(dispatch){
//   axios.get(url)
//       .then((res)=>{
//         console.log("research result",res);
//         dispatch( {
//           type: 'FETCH_RESULT',
//           payload:res.data,
//         })
//
//       });
// }