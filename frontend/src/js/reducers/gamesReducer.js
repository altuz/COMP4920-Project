export default function reducer(state={
    results: JSON.parse(localStorage.getItem('results'))||[],
    discover: JSON.parse(localStorage.getItem('discover'))||[],
    curr: JSON.parse(localStorage.getItem('curr'))||null,
    isSubmitting:false,
    keywords:JSON.parse(localStorage.getItem('keywords'))||{},
  }, action) {

    switch (action.type) {
      case "FETCH_RESULT": {
        localStorage.setItem('results', JSON.stringify(action.payload.results));
        return {
          ...state,
          results: action.payload.results,
          isSubmitting:false,
        }
      }
      case "CLEAR_RESULT": {
        return {
          ...state,
          results:[],
        }
      }
      case "SET_DISCOVER": {
        localStorage.setItem('discover', JSON.stringify(action.payload.results));
        return {
          ...state,
          discover: action.payload.results,
        }
      }
      case "SET_CURR_GAME": {
        localStorage.setItem('curr', JSON.stringify(action.payload));
        return {
          ...state,
          curr: action.payload,
        }
      }
      case "UPDATE_TWEET": {
        const { id, text } = action.payload
        const newTweets = [...state.tweets]
        const tweetToUpdate = newTweets.findIndex(tweet => tweet.id === id)
        newTweets[tweetToUpdate] = action.payload;

        return {
          ...state,
          tweets: newTweets,
        }
      }
      case "DELETE_TWEET": {
        return {
          ...state,
          tweets: state.tweets.filter(tweet => tweet.id !== action.payload),
        }
      }
      case "SEARCHING_GAME":{
        localStorage.setItem('keywords', JSON.stringify(action.payload));
        return {
            ...state,
            keywords:action.payload,
            isSubmitting:true,
        }
      }
    }

    return state
}
