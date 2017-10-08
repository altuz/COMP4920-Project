import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';

@connect((store) => {
  return {
    discover: store.games.discover,
  }
})
export default class Profile extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      gameIndex:this.props.location.state.index,
    }
  }

  componentWillMount() {
    this.props.dispatch({
      type:'SET_CURR_GAME',
      payload: this.props.discover[this.state.gameIndex],
    })
  }



  render () {
    const game = this.props.discover[this.state.gameIndex];
    console.log(game);
    return(
      <div>
       <img src={game.image_url}/>
        fuck you
      </div>
    );
  }
}
