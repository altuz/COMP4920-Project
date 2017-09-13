import React from  "react";
import {Button, Modal} from 'react-bootstrap';




export default class LoginForm extends React.Component {
	render() {
		return(
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
	      			<center>
	      				<h4>Not a member? <a href="#">Sign Up</a> Now!</h4>
	      			</center>
	          </Modal.Body>
		);
	}
}
