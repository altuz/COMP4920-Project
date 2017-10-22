import React from 'react'
import Comment from './Comment.js'

export default class CommentList extends React.Component {
  constructor(props) {
    super(props);
    this.state= {
      limit:5,
    };
    this.loadmore = this.loadmore.bind(this);
    this.collapse = this.collapse.bind(this);
  }

  loadmore(){
    console.log(this.state);
    var vlimit =this.state.limit + 5;
    if(vlimit >= this.props.data.length){
      vlimit = this.props.data.length;
    }
    this.setState({
      limit :vlimit,
    })
  }
  collapse(){
    this.setState({
      limit : 5,
    })
  }


  render() {
    const commentNodes = this.props.data.slice(0,this.state.limit).map((comment,i) => {
      return (
          <Comment author={comment.user_name} rated={comment.rating} key={i}>
            {comment.comment}
          </Comment>
      )
    })
    return (
        <div>
          {commentNodes}
          <div style={{marginLeft: '42%'}}>
            {this.state.limit === this.props.data.length ? (
                <div>
                  <div>There is no more</div>
                  <div className='load-more' onClick={this.collapse}>Collapse</div>
                </div> )
                :(<div className='load-more' onClick={this.loadmore}>Load More</div>)}
          </div>

        </div>
    )
  }
}
