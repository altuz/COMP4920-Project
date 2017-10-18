import React from "react";
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';
import { getProfile } from '../../actions/userActions';
import  { Link } from 'react-router-dom';
import { isFollow } from '../../actions/userActions';
import { follow } from '../../actions/userActions';
import { unfollow } from '../../actions/userActions';

@connect((store) => {
	return {
		user: store.user.user,
		fetched: store.user.fetched,
	};
})

export default class Others extends React.Component {
    constructor(props){
    super(props);
	   this.state= {
		   follow_list:[],
		   gamelist:[],
		   wishlist:[],
		   isfollow: null,
	   };
	   this.Follow = this.Follow.bind(this);
       this.Unfollow = this.Unfollow.bind(this);
    }

    componentWillMount() {
      const user1= this.props.user.user_name;
      const user2= this.props.match.params.user_name;
      console.log(user2);
      isFollow(user1,user2)
        .then((res)=>{
            console.log(res);
            this.setState({
            isfollow:res.data.success,
          })
        })
      console.log("get Profile data");


      getProfile(user2)
        .then((res)=>{
            console.log(res);
           this.setState({
            follow_list:res.data.follows,
            gamelist:res.data.gamelist,
            wishlist:res.data.wishlist,
          })
        })
    }

    imageFormatter(cell,row){
        return (
            <img style={{height:35}} src={cell}/>
        )
    };

    nameFormatter(cell,row,enumObject, index){
        return (
            <div>
                <Link className='game_name' to ={{
                    pathname: `/games/${row.game_id}`,
                    state: {index}
                }}>
                {cell}
                </Link>
            </div>
    )
  }

  profileFormatter(cell,row,enumObject, index){
        return (
            <div>
               <Link className='user_name' to ={{pathname: `/redirect/${row.user_name}`,}}>
               {cell}
               </Link>
            </div>
    )
  }


  Follow(){
    console.log(this.state.isfollow);
    var user={
        user1:this.props.user.user_name,
        user2:this.props.match.params.user_name,
    }
    this.props.dispatch(follow(user));
    this.setState({
      isfollow:"True",
     })

  }

  Unfollow(){
    console.log(this.state.isfollow);
    var user={
        user1:this.props.user.user_name,
        user2:this.props.match.params.user_name,
    }
    this.props.dispatch(unfollow(user));
    this.setState({
      isfollow:"False",
     })

  }


    renderButton = () => {
      console.log(this.state.isfollow);
      if(this.state.isfollow === 'False' ) {
        return (
            <div>
              <Button className = "btn btn-primary followbutton" onClick={() => this.Follow()}>Follow</Button>
            </div>
        )
      }

      return(
            <div>
              <Button className = "btn btn-primary unfollowbutton" onClick={() =>this.Unfollow()}>Unfollow</Button>
            </div>
      )
  }


	render () {
			return(
			<div>
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {this.props.match.params.user_name} </p>
    				<div className='col-md-4'>
                        {this.renderButton()}
                    </div>
    				</div>
    				<Tabs defaultActiveKey={1} className="Tabulation" id="uncontrolled-tab-example">
    					<Tab eventKey={1} title="Playlist">
    						<div>
    						    <BootstrapTable data={this.state.gamelist} hover pagination>
                                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
    					</Tab>
   						<Tab eventKey={2} title="Wishlist">
   						    <div>
    						    <BootstrapTable data={this.state.wishlist} hover pagination>
                                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={3} title="Follow List">
   						    <div>
    						    <BootstrapTable data={this.state.follow_list} hover>
                                    <TableHeaderColumn isKey dataField='user_name' dataFormat={this.profileFormatter}  width='300px'>Username</TableHeaderColumn>
                                    <TableHeaderColumn dataField='num_games'  width='300px'>Number of Games</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   					</Tabs>
			</div>
			);

	}




}