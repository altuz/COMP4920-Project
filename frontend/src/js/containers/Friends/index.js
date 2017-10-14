import React from "react";
import axios from "axios";
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import {Button, Media, Tab, Tabs, Nav} from 'react-bootstrap';
import { search_user } from '../../actions/userActions';

export default class Friends extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username:"",
            result: [],
        }
    }

  profileFormatter(cell,row,enumObject, index){
        return (
            <div>
                <Link className='user_name' to ={{
                    pathname: `/profiles/${row.user_name}`,
                }}>
                {cell}
                </Link>
            </div>
    )
  }


    getResult() {
        search_user(this.state.username)
            .then((res)=>{
            console.log(res);
            this.setState({
            result: res.data.results,
          })
        })
    }

    handleUsernameChange(event) {
        this.setState({"username": event.target.value});
    }


    renderResult = () => {
      if(this.state.result.lenght !== 0 ) {
        return (
            <div>
                <BootstrapTable data={this.state.result} hover>
                <TableHeaderColumn isKey dataField='user_name' dataFormat={this.profileFormatter}  width='300px'>Username</TableHeaderColumn>
                </BootstrapTable>
            </div>
        )
      }
  }



    render (){
      return(
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h2>Friend Search</h2>
                    <div id="custom-search-input">
                        <div class="input-group col-md-12">
                            <input type="text" class="form-control input-lg" placeholder="Enter username" value={this.state.username}
                                    onChange={this.handleUsernameChange.bind(this)}/>
                            <span class="input-group-btn">
                                <button class="btn btn-info btn-lg" type="button" onClick={this.getResult.bind(this)}>
                                    <i class="glyphicon glyphicon-search"></i>
                                </button>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <br/>
            <div id="result">
                {this.renderResult()}
            </div>
        </div>      
      )
    }

}
