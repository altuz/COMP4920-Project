import React, { Component } from 'react'
import { searchGame,clearResult } from '../../actions/userActions.js';
import { Redirect } from 'react-router-dom';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';

@connect((store)=>{
  return {
    results: store.games.results,
  }
})
class SearchBar extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      q:'',
      fetched : false,
    }
    this.isFetched = this.isFetched.bind(this);
  }


  isFetched(){
    this.setState({
      fetched: true,
    })
  }

  handleChange (e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.dispatch(searchGame(this.state.q,this.isFetched));
  }

  render () {
    console.log(this.props.results);
    return (
      <div className='searchbar-container'>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <input
            className='searchbar-input'
            type='text'
            placeholder='Search By game name eg: dota'
            onChange={this.handleChange.bind(this)}
            name='q'
            value={this.state.username} />
        </form>
        {this.state.fetched &&
         <Redirect to={{
           pathname:'/results',
           state: this.props.results,
         }} />
        }
      </div>
    )
  }
}

export default withRouter(SearchBar);


