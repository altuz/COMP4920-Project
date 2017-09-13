import React from "react";
import { Link, Switch, Route, Redirect } from 'react-router-dom';
import { Modal,Button } from "react-bootstrap";


export default class Login extends React.Component {
	  constructor(props) {
     	super(props);

         this.state = {
             showModal: false,
         };
         this.close = this.close.bind(this);
         this.open = this.open.bind(this);
      }

	  close() {
	  	console.log(this.state)
	    this.setState({ showModal: false });
	  }

	  open() {
	  	console.log(this.state)
	    this.setState({ showModal: true });
	  }

	  render() {

	    return (
	      <div>
	        <div onClick={this.open} >
	          Login
	        </div>
	        <Modal show={this.state.showModal} onHide={this.close}>
	          <Modal.Header closeButton>
	            <Modal.Title>Login</Modal.Title>
	          </Modal.Header>
	          <Modal.Body>
	      		<p>to be done</p>
	          </Modal.Body>
	          <Modal.Footer>
	            <Button onClick={this.close}>Close</Button>
	          </Modal.Footer>
	        </Modal>
	      </div>
	    );
	  }
	}

