export default function reducer(state={
    user: JSON.parse(localStorage.getItem('user_info'))||{},
    fetching:  JSON.parse(localStorage.getItem('user_info'))? true:false,
    fetched: JSON.parse(localStorage.getItem('user_info'))? true:false,
    error: null,
  }, action) {
    console.log(action.type);
    switch (action.type) {
      case "FETCH_USER": {
        return {...state, fetching: true}
      }
      case "FETCH_USER_REJECTED": {
        return {...state, fetching: false, error: action.payload}
      }
      case "FETCH_USER_FULFILLED": {
        return {
          ...state,
          fetching: false,
          fetched: true,
          user: action.payload,
        }
      }
      case 'SET_USER': {
        localStorage.setItem('user_info', JSON.stringify(action.payload));
        return {
          ...state,
          user:action.payload,
          fetched:true,
        }
      }
      case "DELETE_USER": {
        localStorage.removeItem('user_info');
        return {
          ...state,
          user: {},
          fetched:false,
        }
      }
    }

    return state
}
