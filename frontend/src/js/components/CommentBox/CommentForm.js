import React from 'react';
import {ModalContainer, ModalDialog} from 'react-modal-dialog';
import { Button } from 'react-bootstrap';
import CommentsubmitForm from './CommentsubmitForm.js'

export default class CommentForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      isShowingModal: false,
    }
    this.handleClick = this.handleClick.bind(this);
    this.handleClose = this.handleClose.bind(this);

  }
  handleClick = () => this.setState({isShowingModal: true});
  handleClose = () => this.setState({isShowingModal: false});

  render() {
    return <div onClick={this.handleClick}>
      <Button className = "btn btn-primary review-btn">Add Review</Button>
      {
        this.state.isShowingModal &&
        <ModalContainer onClose={this.handleClose}>
          <ModalDialog onClose={this.handleClose}>
            <h2 className='review-header'>Write Your Review</h2>
            <CommentsubmitForm handleSubmit={this.props.handleSubmit }/>
          </ModalDialog>
        </ModalContainer>
      }
    </div>;
  }
}