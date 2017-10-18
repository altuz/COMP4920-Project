import React from 'react';
import { Link, Switch, Route, Redirect } from 'react-router-dom';


export default class redirect extends React.Component {
  render() {
    const { user_name }= this.props.match.params;
    console.log(user_name);
    return (
      <div>
       <Redirect to={`/profiles/${user_name}`} />
     </div>
   )
  }
}