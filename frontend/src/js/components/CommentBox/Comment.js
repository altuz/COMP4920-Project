import React, { Component } from 'react'
import Remarkable from 'remarkable'

class Comment extends Component {
  rawMarkup() {
    const md = new Remarkable()
    const rawMarkup = md.render(this.props.children.toString())
    return { __html: rawMarkup }
  }

  render() {
    return (
        <div className='white-container'>
        <div>

          <strong className="commentAuthor">
            {this.props.author}
          </strong>
          {this.props.rated ? (<span className="glyphicon glyphicon-thumbs-up rate-icon"></span>) : (<span className="glyphicon glyphicon-thumbs-down rate-icon"></span>) }
        </div>
          <span dangerouslySetInnerHTML={this.rawMarkup()} />
        </div>
    )
  }
}

export default Comment
