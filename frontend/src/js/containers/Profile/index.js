import React from "react";
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import Edit  from "./EditProfile"
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import { getRecommendation1 } from '../../actions/userActions';
//import { getRecommendation2 } from '../../actions/userActions';
import { getFollowList } from '../../actions/userActions';

@connect((store) => {
	return {
		user: store.user.user,
		gamelist: store.user.game_list,
		wishlist: store.user.wish_list,
		fetched: store.user.fetched,
	};
})

export default class Profile extends React.Component {
	constructor(props){
		super(props);
		this.state= {
		    rec1:[],
		    follow_list: [],
		    //rec2:[],
		};
		this.requestedit = this.requestedit.bind(this);
	}

	requestedit(){
		this.setState({ isedit: true });
	}

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
                <Link className='user_name' to ={{
                    pathname: `/profiles/${row.user_name}`,
                    state: {index}
                }}>
                {cell}
                </Link>
            </div>
    )
  }



  componentWillMount() {
    const username=this.props.user.user_name;
    console.log("rec run");
    getRecommendation1(username)
        .then((res)=>{
            this.setState({
            rec1: res.data.results,
          })
        })
    getFollowList(username)
        .then((res)=>{
            this.setState({
            follow_list: res.data.follows,
            })
         })
    }


/*componentWillMount() {
    const username=this.props.user.user_name;
    console.log("rec run");
    getRecommendation2(username)
        .then((res)=>{
            this.setState({
            rec2: res.data.results,
          })
        })

*/
	imageFormatter(cell,row){
        return (
            <img style={{height:35}} src={cell}/>
        )
    };



	render () {
		if (this.state.isedit){
			return (
			<Edit />
			);
		}

		//get the profile data from backend
		const { user,fetched } = this.props;
		console.log(fetched);
		if(fetched) {
			//get data
			console.log(user.user_name);
			return(
			<div>
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<Button className = "btn btn-primary" type ="submit"  name = "Submit" onClick={this.requestedit}>Edit</Button>
    				</div>
    				<Tabs defaultActiveKey={1} className="Tabulation" id="uncontrolled-tab-example">
    					<Tab eventKey={1} title="Playlist">
    						<div>
    						    <BootstrapTable data={this.props.gamelist} hover pagination>
                                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
    					</Tab>
   						<Tab eventKey={2} title="Wishlist">
   						    <div>
    						    <BootstrapTable data={this.props.wishlist} hover pagination>
                                    <TableHeaderColumn dataField='thumbnail' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={3} title="Popular Recommendation">
   						    <div>
    						    <BootstrapTable data={this.state.rec1} hover>
                                    <TableHeaderColumn dataField='image_url' dataFormat={this.imageFormatter} width = '90px' ></TableHeaderColumn>
                                    <TableHeaderColumn isKey dataField='game_name'  dataFormat={this.nameFormatter} width='300px'>Game Name</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   						<Tab eventKey={4} title="Follow List">
   						    <div>
    						    <BootstrapTable data={this.state.follow_list} hover>
                                    <TableHeaderColumn isKey dataField='user_name'  width='300px'>Username</TableHeaderColumn>
                                    <TableHeaderColumn dataField='num_games'  width='300px'>Number of Game</TableHeaderColumn>
                                </BootstrapTable>
    						</div>
   						</Tab>
   					</Tabs>
			</div>
			);
		}
	}
}