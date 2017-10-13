import React from "react";
import CommentList from './CommentList.js';


export default class CommentBox extends React.Component {
  renderList = () => {
    if(this.props.data.length>0){
      return (
          <CommentList data={this.props.data}/>
      )
    }
    return (
        <div><strong>There is no review</strong></div>
    )
  }
  render (){
    return(
      <div>
        {this.renderList()}
      </div>
    )
  }

}
