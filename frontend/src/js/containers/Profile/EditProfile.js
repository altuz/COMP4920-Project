import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';

@connect((store) => {
	return {
		user: store.user.user,
		fetched: store.user.fetched,
	};
})




export default class EditProfile extends React.Component {


//handle submit and change


	render(){
		const { user,fetched } = this.props;
		console.log(fetched);
		return(
			<div className = "content">
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<form>
    					<div className ="form-group">
    						<label for="email" className="control-label">Email: </label>
    						<input type="email" name="email" className="form-control"/>
    					</div>
    					<div className ="form-group">
    						<label for="password" className="control-label">Password: </label>
    						<input type="password" name="password" className="form-control"/>
    					</div>
    					<div className ="form-group">
    						<label for="confirm" className="control-label">Confirm Password: </label>
    						<input type="password" name="confirm" className="form-control"/>
    					</div>
    					<div className ="form-group">
    						<Button className = "btn btn-primary" type ="submit"  name = "Submit">Save</Button>
    					</div>
    				</form>
    				</div>
			</div>
		)
	}
}
