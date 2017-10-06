import { combineReducers } from "redux"

import user from "./userReducer"
import games from "./gamesReducer"

export default combineReducers({
  games,
  user,
})
