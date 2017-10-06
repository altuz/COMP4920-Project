import React from "react";
// import { connect } from "react-redux";
import { getDiscover } from '../../actions/userActions.js';



export default class Main extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      q:'',
      results:[],
      fetched : false,
    }
  }

  componentWillMount() {
    getDiscover()
    .then((res)=>{
      console.log(res);
    })
  }


  render() {
    return(
      <div >
        <h1>discover</h1>
        <h2>todo: grab data from steam and display on datatables</h2>
      </div>
    );
  }
}
