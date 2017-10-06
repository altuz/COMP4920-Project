export default function reducer(state={
    results: JSON.parse(localStorage.getItem('results'))||[],
  }, action) {

    switch (action.type) {
      case "FETCH_RESULT": {
        localStorage.setItem('results', JSON.stringify(action.payload.results));
        return {
          ...state,
          results: action.payload.results,
        }
      }
      case "CLEAR_RESULT": {
        return {
          ...state,
          results:[],
        }
      }
      case "FETCH_TWEETS_FULFILLED": {
        return {
          ...state,
          fetching: false,
          fetched: true,
          tweets: action.payload,
        }
      }
      case "ADD_TWEET": {
        return {
          ...state,
          tweets: [...state.tweets, action.payload],
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
    }

    return state
}
