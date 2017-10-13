import React from "react";
import SearchBar from '../../components/SearchBar';


export default class Search extends React.Component {
  render() {
    return(
        <div className="front-page">
            <div className='steamrtitle'>
                <img src='static/images/steam-logo.svg' className='search-page-icon' />
                SteamR
            </div>
            <div className='search-bar-int'>
              <div className='input-group search-bar'>
                <SearchBar />
              </div>
            </div>
        </div>
    );
  }
}
