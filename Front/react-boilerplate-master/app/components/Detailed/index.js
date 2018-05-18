import React from 'react';
import { FormattedMessage } from 'react-intl';
import Modal from 'react-modal';

import modalImg from 'images/modal.png';

import axios from 'axios'

import Img from './Img';
import A from './A';
import A2 from './A2';
import A3 from './A3';
import A4 from './A4';
import A5 from './A5';
import A6 from './A6';
import A7 from './A7';
import R from './R';
import R2 from './R2';
import R3 from './R3';
import R4 from './R4';
import R5 from './R5';
import R6 from './R6';
import R7 from './R7';

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

          <Img src={modalImg} />
          <A> Nombre: </A>
          <R> Jorge </R> 
          <A2> Apellido: </A2>
          <R2> Velez </R2>
          <A3> Unidad: </A3>
          <R3> RU1 </R3>
          <A4> Casa: </A4>
          <R4> H1 </R4>
          <A5> Hub: </A5>
          <R5> HUB1 </R5>
          <A6> Lock: </A6>
          <R6> L1 </R6>
          <A7> Email: </A7>
          <R7> j.velez10@uniandes.edu.co </R7>

         <button onClick={this.closeModal}>Close</button>
       </Modal>

      </div>
    );
  }
}

export default Detailed;
