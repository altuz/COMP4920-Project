import { combineReducers } from "redux"

import user from "./userReducer";
import games from "./gamesReducer";
import { reducer as reduxFormReducer } from 'redux-form';

export default combineReducers({
  games,
  user,
  form: reduxFormReducer,
})
