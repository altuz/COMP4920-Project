import React from  "react";
import {Button, Modal} from 'react-bootstrap';
import SignupForm from '../Signup'


export default class LoginForm extends React.Component {
	constructor(props) {
	  super(props);
	   this.state = {
		   issignup: false,
	   };
	   this.requestsignup = this.requestsignup.bind(this);
	}

	requestsignup() {
		this.setState({ issignup: true });
	}

	render() {
		if(this.state.issignup){
			return(
					<div>
						<SignupForm />
					</div>
			);
		}
		return(
			<div>
			<Modal.Header closeButton>
			  <Modal.Title>Login</Modal.Title>
			</Modal.Header>
			<Modal.Body>
				<div className ="form-group">
					<label for="username">Username:
					</label>
					<input type="text" className="form-control" id ="username" placeholder="Enter Username"/>
				</div>
				<div className ="form-group">
					<label for="password">Password:
					</label>
						<input type="password" className="form-control" id ="password" placeholder="Enter Password"/>
				</div>
				<div>
					<p>Not a member? <a style={{color:"blue"}} onClick={this.requestsignup} href="#">Sign Up</a> Now!</p>
				</div>
	          </Modal.Body>
			  <Modal.Footer>
				<Button type = "submit"> Login</Button>
			  </Modal.Footer>
		  	</div>
		);
	}
}
