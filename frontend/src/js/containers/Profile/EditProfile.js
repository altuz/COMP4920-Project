import React from "react";
import {Button, Media, Tab, Nav} from 'react-bootstrap';
import { connect } from 'react-redux';
import Profile from "./index";
import { edit_profile } from '../../actions/userActions.js';

@connect((store) => {
	return {
		user: store.user.user,
		fetched: store.user.fetched,
	};
})




export default class EditProfile extends React.Component {
    constructor(props) {
	  super(props);
	   this.state= {
		   email:'',
		   password:'',
		   confirmpassword:'',
		   isSubmitting:false,
	   };
	   this.onChange = this.onChange.bind(this);
	   this.handleSubmit = this.handleSubmit.bind(this);
	   this.back = this.back.bind(this);
	}


    //handle submit and change
    onChange(e){
		this.setState(
			{[e.target.name]:e.target.value}
		);
	}

	handleSubmit(e){
		e.preventDefault();
		var edit ={
			username:this.props.user.user_name,
			email: this.state.email,
			password:this.state.password
		}
		this.setState({isSubmitting:true});
		this.props.dispatch(edit_profile(edit));
	}

	back(){
	    this.setState({isSubmitting:true});
	    window.location.href='/#/profile';
	}


	render(){
		const { user,fetched } = this.props;
		console.log(fetched);
		if (this.state.isSubmitting == true)
		{
		    return(
		        <Profile />
		    )
		}
		return(
			<div>
					<div className ="media-left">
						<img src = "http://www.ravalyogimatrimony.com/Content/images/default-profile-pic.png" alt = "profile picture"/>
					</div>
					<div className = "media-body">
					<p> Username : {user.user_name} </p>
    				<form onSubmit={this.handleSubmit}  method ="post">
    					<div className ="form-group">
    						<label for="email" className="control-label">Email: </label>
    						<input onChange={this.onChange} type="email" name="email" className="form-control" placeholder={user.email}/>
    					</div>
    					<div className ="form-group">
    						<label for="password" className="control-label">Password: </label>
    						<input onChange={this.onChange} type="password" name="password" className="form-control"/>
    					</div>
    					<div className ="form-group">
    						<label for="confirmpassword" className="control-label">Confirm Password: </label>
    						<input onChange={this.onChange} type="password" name="confirmpassword" className="form-control"/>
    					</div>
    					<div className ="form-group">
    						<Button className = "btn btn-primary" type ="submit"  name = "Submit">Save</Button>
    					</div>
    				</form>
    				    <div className ="form-group">
    						<Button onClick={this.back}className = "btn btn-primary" type ="submit"  name = "Submit">Back</Button>
    					</div>
    				</div>
			</div>
		)
	}
}
