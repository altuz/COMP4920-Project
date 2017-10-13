import React from "react";
import axios from "axios";



export default class Friends extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username:"",
        }
    }

    getResult() {
        const self = this;
        axios.get(`http://127.0.0.1:8000/backend/search_user/?q=` + self.state.username)
            .then(function (response) {
                console.log(response.data.results);
                for (let i = 0; i < response.data.results.length; i++) {
                    let link = document.createElement('a');
                    let br = document.createElement('br');
                    let linkText = document.createTextNode(response.data.results[i].user_name);
                    link.style.color = "black";
                    link.setAttribute('href', "#");
                    link.appendChild(linkText);
                    document.getElementById("result").appendChild(link);
                    document.getElementById("result").appendChild(br);
                }
                self.setState({"username": ""});
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    handleUsernameChange(event) {
        this.setState({"username": event.target.value});
    }

    render (){
      return(
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h2>Friend Search</h2>
                    <div id="custom-search-input">
                        <div class="input-group col-md-12">
                            <input type="text" class="form-control input-lg" placeholder="BaoManFen" value={this.state.username} 
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
            <div id="result">
            </div>
        </div>      
      )
    }

}
