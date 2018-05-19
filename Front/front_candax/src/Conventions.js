import React, { Component } from 'react';
import {Grid, Row, Col, Image} from 'react-bootstrap';


class Conventions extends Component {

  render() {

    return (
      <Grid>
        <Row>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#04B4AE',}}/>
            Normal
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#FF8000',}}/>
            Movimiento detectado
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#DF0101',}}/>
            Puerta abierta
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#0404B4',}}/>
            Bateria baja
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#D7DF01',}}/>
            Numero de intentos claves
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#04B45F',}}/>
            Fallo cerradura
          </Col>
          <Col xs={6} md={4}>
            <Image src="https://images.vexels.com/media/users/3/139342/isolated/preview/61cddf9cfe50f4baaa8f472c253d1cb4-basic-square-outline-by-vexels.png" rounded style={{width: '25px', height: '25px', background:'#088A08',}}/>
            Fallo hub
          </Col>
        </Row>
      </Grid>
    );
  }
}

  export default Conventions;
