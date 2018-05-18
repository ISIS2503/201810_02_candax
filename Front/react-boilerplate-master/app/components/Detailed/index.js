import React from 'react';
import { FormattedMessage } from 'react-intl';
import Modal from 'react-modal';

import axios from 'axios'

const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};


class Detailed extends React.Component { // eslint-disable-line react/prefer-stateless-function
  constructor () {
    super()
    this.state = {
      home: '',
      modalIsOpen: false
    }

    axios.get('http://localhost:8000/house_detail/H1').then(response => this.setState({home: response.data}))

    this.openModal = this.openModal.bind(this);
    this.afterOpenModal = this.afterOpenModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  openModal() {
    this.setState({modalIsOpen: true});
  }

  afterOpenModal() {
    // references are now sync'd and can be accessed.
    this.subtitle.style.color = '#f00';
  }

  closeModal() {
    this.setState({modalIsOpen: false});
  }

  render() {
    return (
      <div>
      <h2 ref={subtitle => this.subtitle = subtitle}>Hello</h2>
        <button onClick={this.openModal}>Open Modal</button>
        <Modal
         isOpen={this.state.modalIsOpen}
         onAfterOpen={this.afterOpenModal}
         onRequestClose={this.closeModal}
         style={customStyles}
         contentLabel="Example Modal"
       >

         <h2 ref={subtitle => this.subtitle = subtitle}>Hello</h2>
         <div>I am a modal</div>
         <form>
           <input />
           <button>tab navigation</button>
           <button>stays</button>
           <button>inside</button>
           <button>the modal</button>
         </form>
         <button onClick={this.closeModal}>Close</button>
       </Modal>

      </div>
    );
  }
}

export default Detailed;
