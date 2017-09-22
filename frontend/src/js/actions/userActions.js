import axios from 'axios';

export function login(user) {
  console.log(user)
  return function(dispatch){
    axios.post('http://localhost:8000/backend/login/',{
        user
    })
    .then((response)=>{
        console.log("ff");
        axios.post('http://localhost:8000/backend/test_session/',{

        }).then((response)=>{
            console.log(response)
        })
    })
    }
}

export function setUserName(name) {
  return {
    type: 'SET_USER_NAME',
    payload: name,
  }
}

export function usersignup() {
  return {
    type: 'SET_USER_AGE',
    payload: age,
  }
}
