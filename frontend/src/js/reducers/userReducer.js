export default function reducer(state={
    user: JSON.parse(localStorage.getItem('user_info'))||{},
    game_list: JSON.parse(localStorage.getItem('game_list'))||{},
    wish_list: JSON.parse(localStorage.getItem('wish_list'))||{},
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
        localStorage.setItem('user_info', JSON.stringify(action.payload.user));
        localStorage.setItem('game_list', JSON.stringify(action.payload.gamelist));
        localStorage.setItem('wish_list', JSON.stringify(action.payload.wishlist));
        return {
          ...state,
          user:action.payload.user,
          game_list:action.payload.gamelist,
          wish_list: action.payload.wishlist,
          fetched:true,
        }
      }
      case "DELETE_USER": {
        localStorage.removeItem('user_info');
        localStorage.removeItem('cookie');
        localStorage.removeItem('game_list');
        localStorage.removeItem('wish_list');
        return {
          ...state,
          user: {},
          fetched:false,
        }
      }
      case "UPDATE_GAMELIST": {
        return {
          ...state,
          game_list: action.payload,
        }
      }
    }

    return state
}
