import React from "react";
import { Link, Switch, Route, Redirect } from 'react-router-dom';
import { Modal,Button, FieldGroup } from "react-bootstrap";
import { connect } from 'react-redux';
import LoginForm from "./LoginForm";
import { logout} from '../../actions/userActions.js';


@connect((store) => {
	return {
		user: store.user.user,
		fetched: store.user.fetched,
	};
})
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


		handleClick(e){
			e.preventDefault();
			this.props.dispatch(logout());
			this.setState({ showModal: false });
			window.location.href='/#/discover';
		}

	  render() {
			const { user,fetched } = this.props;
			console.log(fetched);
			if(fetched) {
				return (
				<div className='user-icon-container'>
					<img src='static/images/user.svg' className='user-icon'/>
					<div className='user-detail logout-user-detail'>
						Hi,{user.user_name}<br/>
						<a href='#0' onClick={this.handleClick.bind(this)} className='login logout logout-font'>Click to logout</a>
					</div>
				</div>
			);
			}
	    return (
     <div>
      	<img src='static/images/user.svg' className='user-icon'/>
        <div className='user-detail'>
          <a href='#' onClick={this.open} className='login logout'>Please Login</a>
        </div>
         <div>
	        <Modal show={this.state.showModal} onHide={this.close}>
			  <LoginForm/>
	        </Modal>
	      </div>
      </div>
	    );
	  }
}
