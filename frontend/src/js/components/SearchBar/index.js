import React, { Component } from 'react'
import { searchGame,clearResult } from '../../actions/userActions.js';
import { Redirect } from 'react-router-dom';
import { withRouter } from 'react-router';


class SearchBar extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      q:'',
      results:[],
      fetched : false,
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
      this.setState({
        results:res.data.results,
        fetched:true,
      });

    })
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
        {this.state.fetched &&
         <Redirect to={{
           pathname:'/results',
           state:this.state.results,
         }} />
        }
      </div>
    )
  }
}

export default withRouter(SearchBar);


