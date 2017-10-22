import React from "react";
import {Button, Modal} from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { signup } from '../../actions/userActions.js';
import { connect } from 'react-redux';
@connect((store)=>{
    return store.user;
})


export default class SignupForm extends React.Component {
    constructor(props){
        super(props);
        this.state = {
                username:'',
                email:'',
                password:'',
                passwordconfirm:'',
                privacy: false,
                invalid: false,
                isSubmitting:false,
                errors: {},
                issuccess: 0
        }
        this.handleSubmit = this.handleSubmit.bind(this);
        this.onChange = this.onChange.bind(this);
        this.checkPassword = this.checkPassword.bind(this);
        this.isFail = this.isFail.bind(this);
    }

    onChange(e){
      this.setState(
            {[e.target.name]:e.target.value}
        );
    }

    checkPassword()
    {
        if (this.state.password == this.state.passwordconfirm)
        {
            return true;
        }
        else{
            return false;
        }

    }
    isFail() {
    this.setState({
      isSubmitting:false,
      issuccess:2
    })
  }


    handleSubmit(e){
      e.preventDefault();
      if (checkPassword()){
            var user={
            user_name : this.state.username,
            email : this.state.email,
            pass_word : this.state.password,
            privacy : this.state.privacy
        }
        this.setState({isSubmitting:true});
        this.setState({issuccess:1});
        this.props.dispatch(signup(user,this.isFail));
      }
      else{
        this.setState({issuccess:2});
      }

      }

    render()
    {
        if(this.state.issuccess == 0)
        {
            return(
                <div>
                <Modal.Header closeButton>
                    <Modal.Title>Signup</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                <form onSubmit={this.handleSubmit}  method ="post">
                    <div className ="form-group">
                        <label for="username" className="control-label">Username:</label>
                        <input onChange={this.onChange} type="text" className="form-control" name= "username" placeholder="Enter Username"/>
                    </div>
                    <div className ="form-group">
                        <label for="email" className="control-label">Email:</label>
                        <input onChange={this.onChange} type="text" name="email" className="form-control" placeholder="Enter email"/>
                    </div>
                    <div className ="form-group">
                        <label for="password" className="control-label">Password: </label>
                        <input onChange={this.onChange} type="password" name ="password" className="form-control" placeholder="Enter Password"/>
                    </div>
                    <div className ="form-group">
                        <label for="password" className="control-label">Confirm Password: </label>
                        <input onChange={this.onChange} type="password" name= "passwordconfirm" className="form-control" placeholder="Enter Password again"/>
                    </div>
                    <div className="form-group">
                    <Button type = "submit" name="Submit"> Signup</Button>
                    {this.state.isSubmitting ?<img src='static/images/loading.svg' height="50" width="50"/>:""}
                    </div>
                </form>
                </Modal.Body>
                </div>
                );
        }
        if(this.state.issuccess == 1)
        {
            return(
                <div>
                <Modal.Header closeButton>
                    <Modal.Title>Signup</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p> Confirm the verification email please</p>
                </Modal.Body>
                </div>
                );
        }

        if(this.state.issuccess == 2)
        {
            return(
                <div>
                <Modal.Header closeButton>
                    <Modal.Title>Signup</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p> Registration failed please redo</p>
                </Modal.Body>
                </div>
                );
        }

    }

}

