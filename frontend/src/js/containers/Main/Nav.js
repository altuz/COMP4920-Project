import React from "react";
import Login from '../../components/Login';
import { Link, Switch, Route } from 'react-router-dom';

class Header extends React.Component {
	render(){
		return(
			 <header className='header'>
        		<div className='logo'>
	          		<Link to='/'>
	          		<img src='static/images/steamRlogo.svg' className='logo-icon'/>
		            SteamR
	          		</Link>
       			</div>

      		</header>
	 )
	}
}


export default class Nav extends React.Component {
  render() {
    return(
    	<div>
    	<Header />
		 <nav className='side-nav'>
	        <ul>
	          <li className='user'>
	            <Login />
	          </li>
	      </ul>
		</nav>
		</div>
    );
  }
}

