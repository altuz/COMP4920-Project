import React from 'react'
import Comment from './Comment.js'

export default class CommentList extends React.Component {
  render() {
    const commentNodes = this.props.data.map((comment,i) => {
      return (
          <Comment author={comment.user_name} rated={comment.rating} key={i}>
            {comment.comment}
          </Comment>
      )
    })
    return (
        <div>
          {commentNodes}
        </div>
    )
  }
}
