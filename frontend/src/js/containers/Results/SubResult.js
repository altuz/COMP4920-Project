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
    console.log(this.props.match);
      // this.props.dispatch({
      //   type:'SET_CURR_GAME',
      //   payload: this.props.discover[this.state.gameIndex],
      // })
  }



  render () {
    return(
      <div>
       {/*<img src={game.image_url}/>*/}
        {/*{game.game_description}*/}
      </div>
    );
  }
}
