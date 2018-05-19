import React, { Component } from 'react';
import {Carousel} from 'react-bootstrap';
// import { React_Bootstrap_Carousel } from "react-bootstrap-carousel";
// import "bootstrap/dist/css/bootstrap.css";
// import "react-bootstrap-carousel/dist/react-bootstrap-carousel.css";

class ControlledCarousel extends Component {
  render() {
    return (
      <Carousel style={{width: '100%', height: '80%'}}>
        <Carousel.Item>
          <img style={{width: '100%', height: '80%'}}  alt='img1' src="http://www.desktop-screens.com/data/out/67/3094821-lock-wallpapers.jpg" />
          <Carousel.Caption style= {{width: '30%', height: '60%'}}>
            <h3>Seguridad</h3>
            <p>Yale tiene una amplia covertura que garantiza la seguridad de tu hogar</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img style={{width: '100%', height: '100%'}} alt='img2' src="https://images.pexels.com/photos/374710/pexels-photo-374710.jpeg?auto=compress&cs=tinysrgb&h=350" />
          <Carousel.Caption style={{width: '60%', height: '70%'}}>
            <h3>Facilidad</h3>
            <p>Abre la puerta de tu casa sin problemas, sin limites, sin restricciones</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img style={{width: '100%', height: '100%'}}  alt='img3' src="http://www.hdwallpaperup.com/wp-content/uploads/2015/12/Light-Blue-Violet-Color-Abstract-Wallpaper-1600x900.jpg" />
          <Carousel.Caption style={{width: '60%', height: '80%'}}>
            <h3>Innovación</h3>
            <p>Tecnología de última generación para monitorear el hogar</p>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
    );
  }
}

export default ControlledCarousel;
