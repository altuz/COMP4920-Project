import { combineReducers } from "redux"

import user from "./userReducer";
import games from "./gamesReducer";
import { reducer as reduxFormReducer } from 'redux-form';
import { reducer as notifReducer } from 'redux-notifications';



export default combineReducers({
  games,
  user,
  form: reduxFormReducer,
  notifs: notifReducer,
})
