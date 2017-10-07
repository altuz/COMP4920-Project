import React from "react";
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import Edit  from "./EditProfile"
import { connect } from 'react-redux';



export default class Profile extends React.Component {
	constructor(props){
		super(props);
		this.state= {
            isedit: false,
		};
		this.requestedit = this.requestedit.bind(this);
	}

	requestedit(){
		this.setState({ isedit: true });
	}



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
			<div className = "content">
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<Button className = "btn btn-primary" type ="submit"  name = "Submit" onClick={this.requestedit}>Edit</Button>
    				</div>
    				<Tabs defaultActiveKey={1} className="String" id="uncontrolled-tab-example">
    					<Tab eventKey={1} title="Playlist">
    						<li>Tab 1 content</li>
    					</Tab>
   						<Tab eventKey={2} title="Wishlist">Tab 2 content</Tab>
   					</Tabs>
			</div>
			);
		}
	}
}
