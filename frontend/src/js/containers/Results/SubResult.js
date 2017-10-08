import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';
import { getGameInfo } from '../../actions/userActions'
import { add_to_game_list,add_to_wish_list } from '../../actions/gamesActions'


@connect((store) => {
  return {
    user: store.user.user,
    user_fetched: store.user.fetched,

  }
})
export default class Profile extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      curr_game:[],
      is_my_game:null,
      is_my_wish:null,
    }
    this.add_to_game_list = this.add_to_game_list.bind(this);
    this.add_to_wish_list = this.add_to_wish_list.bind(this);
  }

  componentWillMount() {
    var username =''
    if(this.props.user_fetched){
      username=this.props.user.user_name;
    }
    const gameID=this.props.match.params.gameID;
    getGameInfo(gameID,username)
        .then((res)=>{
          this.setState({
            curr_game:res.data.game_info,
            in_my_game: res.data.in_game_list,
            in_my_wish: res.data.in_wish_list,
          })

        })
  }

  add_to_game_list(){
    console.log(this.state.curr_game);
    this.props.dispatch(add_to_game_list(this.props.user.user_name,this.state.curr_game[0].game_id));
    this.setState({
      in_my_game: true,
      in_my_wish: false,
    })

  }

  add_to_wish_list(){
    console.log(this.state.curr_game);
    this.props.dispatch(add_to_wish_list(this.props.user.user_name,this.state.curr_game[0].game_id));
    this.setState({
      in_my_wish: true,
      in_my_game: false,
    })
  }


  rawMarkup(){
    var rawMarkup = this.state.curr_game[0].game_description;
    return { __html: rawMarkup };
  }

  renderButton = () => {
      if(this.props.user_fetched && !this.state.in_my_game && !this.state.in_my_wish) {
        return (
            <div>
              <Button className = "btn btn-primary gamebutton" onClick={this.add_to_game_list} >Add to Game List</Button>
              <br/>
              <Button className = "btn btn-primary wishbutton" onClick={this.add_to_wish_list} >Add to Wish List</Button>
            </div>
        )
      }
      if(this.props.user_fetched && this.state.in_my_game && !this.state.in_my_wish) {
      return (
          <div>
            <Button className = "btn btn-default gamebutton" >Remove From Game List</Button>
          </div>
      )
    }
    if(this.props.user_fetched && !this.state.in_my_game && this.state.in_my_wish) {
      return (
          <div>
            <Button className = "btn btn-primary gamebutton" onClick={this.add_to_game_list}>Add to Game List</Button>
            <br/>
            <Button className = "btn btn-default wishbutton" >Remove From Wish List</Button>
          </div>
      )
    }
  }


  render () {

    if(this.state.curr_game.length>0){
      const game=this.state.curr_game[0];
      return(
          <div className='row'>
            <div className='col-md-8'>
              <img className='description-img' src={game.image_url}/>
              <div dangerouslySetInnerHTML={this.rawMarkup()}></div>
            </div>
            <div className='col-md-4'>
                {this.renderButton()}
            </div>
          </div>
      );
    }
    return null;
  }
}
