import React from "react";
import {Button, Modal} from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { signup } from '../../actions/userActions.js';
import { connect } from 'react-redux';
import classnames from 'classnames';
import validateInput from '../../function/signupvalidation';



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
    }

    onChange(e){
      this.setState(
            {[e.target.name]:e.target.value}
        );
    }


     isValid() {
        const { errors, isValid } = validateInput(this.state);

        if(!isValid) {
            this.setState({ errors });
        }

        return isValid;
      }

    handleSubmit(e){
      e.preventDefault();
        var user={
            user_name : this.state.username,
            email : this.state.email,
            pass_word : this.state.password,
            privacy : this.state.privacy
        }
        this.setState({isSubmitting:true});
        this.props.dispatch(signup(user));
        this.setState({issuccess:1})
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
                    <div className ={classnames('form-group', {'has-error': errors.email})}>
                        <label className="control-label">Email:</label>
                        <input onChange={this.onChange} type="text" className="form-control" id ="email" name="email" placeholder="Enter email"/>
                        {errors.email && <span className="help-block">{errors.email}</span>}
                    </div>
                    <div className ={classnames('form-group', {'has-error': errors.password})}>
                        <label className="control-label">Password: </label>
                        <input onChange={this.onChange} type="password" className="form-control" id ="password" name="password" placeholder="Enter Password"/>
                        {errors.password && <span className="help-block">{errors.password}</span>}
                    </div>
                    <div className ={classnames('form-group', {'has-error': errors.passwordconfirm})}>
                        <label className="control-label">Confirm Password: </label>
                        <input onChange={this.onChange} type="password" className="form-control" id ="passwordconfirm" name="passwordconfirm" placeholder="Enter Password again"/>
                        {errors.passwordconfirm && <span className="help-block">{errors.passwordconfirm}</span>}
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

