import React, { Component } from 'react';
import {Navbar, Nav, NavItem} from 'react-bootstrap';
import MiModal from './Modal1';

class NavBar extends Component {

  render() {

    return (
      <div>
          <MiModal/>
          <Navbar>
            <Nav>
                <NavItem href="/">Todas</NavItem>
                <NavItem href="/motion">Movimiento detectado </NavItem>
                <NavItem href="/door">Puerta abierta  </NavItem>
                <NavItem href="/battery">Bateria Baja </NavItem>
                <NavItem href="/number">Claves</NavItem>
                <NavItem href="/lock">Fallo cerradura</NavItem>
                <NavItem href="/hub">Fallo hub </NavItem>
            </Nav>
          </Navbar>
      </div>
    );
  }
}

  export default NavBar;
