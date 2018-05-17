import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from './A';
import Img from './Img';
import ImgBack from './ImgBack';
import NavBar from './NavBar';
import HeaderLink from './HeaderLink';
import Banner from 'images/nightSky.png';
import logo from 'images/yaleLogo.png';
import messages from './messages';

class Header extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (



      <div>
        <A>
        <ImgBack src={Banner} alt="react-boilerplate - Logo" />
        <Img src={logo} />
        </A>
        
        <NavBar>
          <HeaderLink to="/">
            <FormattedMessage {...messages.home} />
          </HeaderLink>
        </NavBar>
      </div>
    );
  }
}

export default Header;
