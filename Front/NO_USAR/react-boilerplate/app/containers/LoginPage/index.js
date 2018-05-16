/*
 * FeaturePage
 *
 * List all the features
 */
import React from 'react';
import { Helmet } from 'react-helmet';
import { FormattedMessage } from 'react-intl';
import { Component } from 'react';
import { Navbar, Button } from 'react-bootstrap';

import H1 from 'components/H1';
import messages from './messages';
import List from './List';
import ListItem from './ListItem';
import ListItemTitle from './ListItemTitle';
import Auth from './Auth.js';
import history from './history.js'

export default class LoginPage extends React.Component { // eslint-disable-line react/prefer-stateless-function

  // Since state and props are static,
  // there's no need to re-render this component
  shouldComponentUpdate() {
    return false;
  }

  render() {
    // const auth = new Auth();
    // auth.login()
    return (
      <div>
        <Helmet>
          <title>Login Page</title>
          <meta name="description" content="Login page of React.js Boilerplate application" />
        </Helmet>
      </div>
    );
  }
}
