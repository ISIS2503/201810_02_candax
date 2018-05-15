/**
 *
 * App
 *
 * This component is the skeleton around the actual pages, and should only
 * contain code that should be seen on all pages. (e.g. navigation bar)
 */

import React from 'react';
import { Helmet } from 'react-helmet';
import styled from 'styled-components';
import { Switch, Route, Router } from 'react-router-dom';
import registerServiceWorker from './registerServiceWorker';
import ReactDOM from 'react-dom';

import HomePage from 'containers/HomePage/Loadable';
import FeaturePage from 'containers/FeaturePage/Loadable';
import NotFoundPage from 'containers/NotFoundPage/Loadable';
import LoginPage from 'containers/LoginPage/Loadable';
import LogoutPage from 'containers/LogoutPage/Loadable';
import Callback from 'containers/Callback/Loadable';
import Header from 'components/Header';
import Footer from 'components/Footer';
import Auth from 'containers/LoginPage/Auth';
import history from 'containers/LoginPage/history';

const AppWrapper = styled.div`
  max-width: calc(768px + 16px * 2);
  margin: 0 auto;
  display: flex;
  min-height: 100%;
  padding: 0 16px;
  flex-direction: column;
`;

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}

export default function App() {
  return (
    <AppWrapper>
      <Helmet
        titleTemplate="%s - React.js Boilerplate"
        defaultTitle="React.js Boilerplate"
      >
        <meta name="description" content="A React.js Boilerplate application" />
      </Helmet>
      <Header />
        <Router history={history} component={HomePage}>
          <div>
            <Route exact path="/" render={(props) => <HomePage auth={auth} {...props} />} />
            <Route path="/HomePage" render={(props) => <HomePage auth={auth} {...props} />} />
            <Route path="/login" render={(props) => <LoginPage auth={auth} {...props} />} />
            <Route path="/callback" render={(props) => {
              handleAuthentication(props);
              return <Callback {...props} />
            }}/>
          </div>
        </Router>
      <Footer />
    </AppWrapper>
  );
}
