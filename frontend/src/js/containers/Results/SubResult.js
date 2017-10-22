import React from "react";
import { Button } from 'react-bootstrap';
import { connect } from 'react-redux';
import { getGameInfo } from '../../actions/userActions';
import { add_to_game_list,add_to_wish_list,remove_from_game_list,send_review } from '../../actions/gamesActions'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import CommentBox from '../../components/CommentBox';
import CommentForm from '../../components/CommentBox/CommentForm.js';


@connect((store) => {
  return {
    user: store.user.user,
    user_fetched: store.user.fetched,
    form: store.form.simple,
  }
})
export default class Profile extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      curr_game:[],
      is_my_game:null,
      is_my_wish:null,
      reviews_list:[],
      user_review:[],
      genre_list:[],
      category_list:[],
      isSubmitting:false,
    }
    this.add_to_game_list = this.add_to_game_list.bind(this);
    this.add_to_wish_list = this.add_to_wish_list.bind(this);
    this.remove_from_game_list=this.remove_from_game_list.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  //send_review(form, username, gameid)
  handleSubmit() {
    this.setState({
      isSubmitting:true,
    })
    const gameID=this.props.match.params.gameID;
    send_review(this.props.form, this.props.user.user_name,gameID)
    window.location.reload();
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
            reviews_list: res.data.reviews_list,
            user_review :res.data.user_review,
            genre_list:res.data.genre_list,
            category_list:res.data.category_list,
          })

        })
  }

  add_to_game_list(){
    this.props.dispatch(add_to_game_list(this.props.user.user_name,this.state.curr_game[0].game_id));
    this.setState({
      in_my_game: true,
      in_my_wish: false,
    })

  }

  add_to_wish_list(){
    this.props.dispatch(add_to_wish_list(this.props.user.user_name,this.state.curr_game[0].game_id));
    this.setState({
      in_my_wish: true,
      in_my_game: false,
    })
  }

  remove_from_game_list(){
    this.props.dispatch(remove_from_game_list(this.props.user.user_name,this.state.curr_game[0].game_id));
    this.setState({
      in_my_wish: false,
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
            <Button className = "btn btn-default gamebutton" onClick={this.remove_from_game_list } >Remove From Game List</Button>
          </div>
      )
    }
    if(this.props.user_fetched && !this.state.in_my_game && this.state.in_my_wish) {
      return (
          <div>
            <Button className = "btn btn-primary gamebutton" onClick={this.add_to_game_list} >Add to Game List</Button>
            <br/>
            <Button className = "btn btn-default wishbutton" onClick={this.remove_from_game_list} >Remove From Wish List</Button>
          </div>
      )
    }
  }

  renderGenres(){
    const mapGenre = this.state.genre_list.map((genre,i)=>{
      return (<div key={i}><span className="badge" >{genre}</span></div>)
    })

    return(<div>{mapGenre}</div>)
  }

  renderCategory(){
    const mapCategory = this.state.category_list.map((category,i)=>{
      return (<div key={i}><span className="badge" >{category}</span></div>)
    })

    return(<div>{mapCategory}</div>)
  }


  render () {
    console.log(this.state);
    if(this.state.curr_game.length>0){
      const game=this.state.curr_game[0];
      return(
          <div className='row'>
            <div className='col-md-9'>
              <img className='description-img' src={game.image_url} height='400px'/>
              <div className='page-tabs'>
              <Tabs>
                <TabList>
                  <Tab><h5>Game Description</h5></Tab>
                  <Tab><h5>Reviews</h5></Tab>
                  {this.props.user_fetched ? (<Tab><h5>My review</h5></Tab>) : null}
                </TabList>
                <TabPanel>
                  <div className='testing' dangerouslySetInnerHTML={this.rawMarkup()}></div>
                </TabPanel>
                <TabPanel>
                  <div>
                    <CommentBox data={this.state.reviews_list}/>
                  </div>
                </TabPanel>
                {this.props.user_fetched ? (
                <TabPanel>
                <div>
                  {this.state.in_my_game ? <CommentBox data={this.state.user_review}/> : null}
                  <CommentForm handleSubmit={this.handleSubmit}
                               user_review={this.state.user_review}
                               isSubmitting={this.state.isSubmitting}
                               in_my_game={this.state.in_my_game}
                  />
                </div>
              </TabPanel>)  : null}
              </Tabs>
              </div>

            </div>
            <div className='col-md-3'>
                {this.renderButton()}
                <div className='genre'>Genres:</div>
                <div className='genre-container'>
                    {this.renderGenres()}
                </div>
              <div className='category'>Categories:</div>
              <div className='genre-container'>
                {this.renderCategory()}
              </div>
            </div>
          </div>
      );
    }
    return null;
  }
}
