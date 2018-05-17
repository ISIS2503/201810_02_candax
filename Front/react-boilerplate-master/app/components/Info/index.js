import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from './A';
import A2 from './A2';
import A3 from './A3';
import Img from './Img';
import Img2 from './Img2';
import Img3 from './Img3';

import logoCan from 'images/candax.png';
import logoYale from 'images/yaleLogo.png';
import partnership from 'images/partnership.png';


class Header extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (



      <div>

        <Img3 src={partnership}  />
        <Img2 src={logoCan}  />
        <Img src={logoYale} />

        <A> Somos parte del Grupo ASSA ABLOY, la mayor compañía de cerraduras del
        mundo reconocida como líder mundial en soluciones de apertura de puertas.
        Yale Connect permite abrir y cerrar dispositivos Yale como cerraduras digitales,
        cerraduras eléctricas y electroimanes de forma remota y segura con un teléfono inteligente,
        tableta u ordenador a través de una aplicación gratuita disponible para IOS y Android.
        Desde cualquier parte del mundo, con una conexión a internet, es posible abrir y cerrar
        las puertas de tu hogar u oficina. </A>
        <A2>  Somos un grupo de estudiantes de Ingeniería de Sistemas y Computación de la Universidad de los
        Andes interesados en el desarrollo de aplicaciones y su arquitectura. </A2>

        <A3> AAA </A3>

      </div>


    );
  }
}

export default Header;
