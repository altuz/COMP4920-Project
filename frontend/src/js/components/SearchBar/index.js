import React, { Component } from 'react'
import { searchGame,clearResult } from '../../actions/userActions.js';
import { Redirect } from 'react-router-dom';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';
import Select from 'react-select-2';
import categories from './category_list.json';
import genres from './genre_list.json';
import { Button } from 'react-bootstrap';
const category = categories.category_list;
const genre = genres.genre_list;


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
      test:'',
      fetched : false,
      selected_category: [],
      selected_genre:[],
    }
    this.isFetched = this.isFetched.bind(this);
    this.handleSelect_category_Change = this.handleSelect_category_Change.bind(this);
    this.handleSelect_genre_Change = this.handleSelect_genre_Change.bind(this);
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
    console.log(this.state);
    this.props.dispatch(searchGame(this.isFetched,this.state));
  }

  handleSelect_category_Change (selected_category) {
    console.log('You\'ve selected:', selected_category);
    this.setState({ selected_category });
    console.log(this.state.selected_category);
  }

  handleSelect_genre_Change (selected_genre){
    console.log('You\'ve selected:', selected_genre);
    this.setState({ selected_genre });
    console.log(this.state.selected_genre);
  }

  render () {
    return (
      <div className='searchbar-container'>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <input
            className='searchbar-input'
            type='text'
            placeholder='Search By game name eg: dota'
            onChange={this.handleChange.bind(this)}
            name='q'
            value={this.state.q} />
          <div className='select-input'>
            <Select
              multi
              placeholder="Select category"
              simpleValue
              options={category}
              onChange={this.handleSelect_category_Change}
              value={this.state.selected_category}
            />
            <div className='second-select'>
              <Select
                  multi
                  placeholder="Select genre"
                  simpleValue
                  options={genre}
                  onChange={this.handleSelect_genre_Change}
                  value={this.state.selected_genre}
              />
            </div>
          </div>
          <div className="form-group search-btn">
            <Button className='btn btn-primary btn-md' type="submit" name="Submit"> Search</Button>
          </div>
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


