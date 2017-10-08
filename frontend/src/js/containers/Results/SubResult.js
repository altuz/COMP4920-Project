import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';
import { getGameInfo } from '../../actions/userActions'

@connect((store) => {
  return {
    discover: store.games.discover,
  }
})
export default class Profile extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      curr_game:[]
    }
  }

  componentWillMount() {
    const gameID=this.props.match.params.gameID;
    getGameInfo(gameID)
        .then((res)=>{
          this.setState({
            curr_game:res.data.game_info,
          })
        })
      // this.props.dispatch({
      //   type:'SET_CURR_GAME',
      //   payload: this.props.discover[this.state.gameIndex],
      // })
  }

  rawMarkup(){
    var rawMarkup = this.state.curr_game[0].game_description;
    return { __html: rawMarkup };
  }


  render () {

    if(this.state.curr_game.length>0){
      const game=this.state.curr_game[0];
      return(
          <div className='col-md-4'>
            <img src={game.image_url}/>
            <div dangerouslySetInnerHTML={this.rawMarkup()}></div>
          </div>
      );
    }
    return null;
  }
}
