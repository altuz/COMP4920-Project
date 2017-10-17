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
      if(this.state.result.length !== 0 ) {
        return (
            <div className="col-md-6 friends-result">
                <BootstrapTable data={this.state.result} hover pagination={true}>
                <TableHeaderColumn isKey dataField='user_name' dataFormat={this.profileFormatter}  width='300px'>Username</TableHeaderColumn>
                </BootstrapTable>
            </div>
        )
      }
      return null
  }



    render (){
      return(
        <div className="container">
            <div className="row">
                <div className="col-md-6">
                    <h2>Friend Search</h2>
                    <div id="custom-search-input">
                        <div className="input-group col-md-12">
                            <input type="text" class="form-control input-lg" placeholder="Enter username" value={this.state.username}
                                    onChange={this.handleUsernameChange.bind(this)}/>
                            <span className="input-group-btn">
                                <button className="btn btn-info btn-lg" type="button" onClick={this.getResult.bind(this)}>
                                    <i className="glyphicon glyphicon-search"></i>
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