import React, { Component } from 'react'
import { searchGame } from '../../actions/userActions.js';



export default class SearchBar extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      q:''
    }
  }

  handleChange (e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    searchGame(this.state.q)
    .then((res)=>{
      console.log(res);
    })
    .catch((err)=>{
      console.log(err);
    });
  }

  render () {
    return (
      <div className='searchbar-container'>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <input
            className='searchbar-input'
            type='text'
            placeholder='Search By game name'
            onChange={this.handleChange.bind(this)}
            name='q'
            value={this.state.username} />
        </form>
      </div>
    )
  }
}
