import React, { Component }  from 'react';
import {Modal, Button, OverlayTrigger} from 'react-bootstrap';
import Websocket from 'react-websocket';




class MiModal extends Component {
    constructor(props, context) {
      super(props, context);
  
      this.handleShow = this.handleShow.bind(this);
      this.handleClose = this.handleClose.bind(this);
  
      this.state = {
        show: false,
        mensaje : "",
        titulo : "",
        
      };
    }
  
    handleClose() {
      this.setState({ show: false });
    }
  
    handleShow() {
      this.setState({ show: true });
    }
    handleData(data) {
      var dataParsed = JSON.parse(data)
      console.log(dataParsed);
      console.log(dataParsed.owner);
      var tit = "";
      var casita = "";
      var res = "";
      var msg = "";
    
      res = dataParsed.res_unit;
      casita = dataParsed.house; 


      if(dataParsed.data == "Door"){
        tit = "Puerta Abierta";
        msg = "Hay una puerta abierta en la unidad residencial: " + res + " en la casa: " + casita + ".";

      }
      else if(dataParsed.data == "Low"){
        tit = "Batería baja";
        msg = "Una de las alarmas en la casa: " + casita + " de la unidad residencial: " + res + " tiene poca batería.";

      }
      else if(dataParsed.data == "Motion"){
        tit = "Movimiento detectado";
        msg = "Movimiento detectado en la casa: "+ casita + " de la unidad residencial: " + res + ".";
      }
      else if(dataParsed.data == "Hub" ){
        tit = "Hub fuera de linea";
        msg = "Hub fuera de linea en la casa: " + casita + " de la unidad residencial: " + casita + ".";

      }
      else if(dataParsed.data == "Number"){
        tit = "Número de intentos excedido";
        msg = "Se han excedido el número de intentos en la casa: " + casita + " de la unidad residencial: " + casita + ".";;
      }
      else if(dataParsed.data == "Cerradura"){
        tit = "Cerradura fuera de línea";
        msg = "Cerrado fuera de line en la casa: " + casita + " de la unidad residencial: " + casita + ".";
      }
      this.setState({titulo: tit, mensaje:msg});
      console.log(this.state.titulo);
      console.log(this.state.mensaje);
      this.handleShow();
    }
  
  
    render() {
 
     
      return (
        <div>
         
         <Websocket url='ws://localhost:8000/socketAlarms' onMessage={this.handleData.bind(this)}/>
          <Modal show={this.state.show} onHide={this.handleClose} style={{ background:'#FF8000'}}>
            <Modal.Header closeButton>
              <Modal.Title>{this.state.titulo}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              
              <p>
                {this.state.mensaje}
              </p>
  
              
              
            </Modal.Body>
            <Modal.Footer>
              <Button onClick={this.handleClose}>Close</Button>
            </Modal.Footer>
          </Modal>
        </div>
      );
    }
  }
  
//   render(<MiModal />);
  

  export default MiModal;
