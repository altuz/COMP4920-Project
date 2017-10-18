import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { HashRouter as Router, Route,Switch } from 'react-router-dom';

import Main from "./containers/Main"
import store from "./store"

const app = document.getElementById('app');


class App extends React.Component{
	render(){
		return(			
			<Provider store={store}>
				<div>
				 <Router>
							<Switch>
								<Route path='/' component={Main} />
							</Switch>
				 </Router>
				</div>
		 </Provider>

		);
	}
}


ReactDOM.render(<App/>, app);
