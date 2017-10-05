import React, { Component } from 'react'

class SearchBar extends Component {
  constructor (props) {
    super(props)
    this.state = {
      gamename:''
    }
  }

  handleChange (e) {
    this.setState({ [e.target.name]: e.target.value });
    console.log(this.state.gamename);
  }

  render () {
    return (
      <div className='searchbar-container'>
        <form onSubmit={e => e.preventDefault()}>
          <input
            className='searchbar-input'
            type='text'
            placeholder='Search By game name'
            onChange={this.handleChange.bind(this)}
            name='gamename'
            value={this.state.username} />
        </form>
      </div>
    )
  }
}

export default SearchBar
