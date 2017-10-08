import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';
import { getGameInfo } from '../../actions/userActions'

@connect((store) => {
  return {
    user_fetched: store.user.fetched,
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

  renderButton = () => {
      if(this.props.user_fetched) {
        return (
            <div>
              <Button className = "btn btn-primary gamebutton" >Add to Game List</Button>
              <br/>
              <Button className = "btn btn-primary wishbutton" >Add to Wish List</Button>
            </div>
        )
      }
  }


  render () {

    if(this.state.curr_game.length>0){
      const game=this.state.curr_game[0];
      return(
          <div className='row'>
            <div className='col-md-7'>
              <img className='description-img' src={game.image_url}/>
              <div dangerouslySetInnerHTML={this.rawMarkup()}></div>
            </div>
            <div className='col-md-5'>
                {this.renderButton()}
            </div>
          </div>
      );
    }
    return null;
  }
}
