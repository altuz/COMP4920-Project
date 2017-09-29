import axios from 'axios';

export function login(user) {
  return function(dispatch){
    axios.post('http://localhost:8000/backend/login/',{
        user
    })
    .then((response)=>{
        if(response.data.message==='success'){
            dispatch( {
              type: 'SET_USER',
              payload:response.data.user,
            })
        }
    })
    }
}

export function logout(){
  return {
    type: 'DELETE_USER',
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
