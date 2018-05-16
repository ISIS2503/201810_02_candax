import React from 'react';
import { Route, Router } from 'react-router-dom';
import HomePage from 'containers/HomePage/Loadable';
import LoginPage from 'containers/LoginPage/Loadable'
import Callback from 'containers/Callback/Loadable';
import Auth from 'containers/LoginPage/auth';
import history from 'containers/LoginPage/history';

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}

const Routes = () => (
  <Router history={history} component={HomePage}>
    <div>
      <Route exact path="/" render={(props) => <HomePage auth={auth} {...props} />} />
      <Route path="/home" render={(props) => <HomePage auth={auth} {...props} />} />
      <Route path="/login" render={(props) => <LoginPage auth={auth} {...props} />} />
      <Route path="/callback" render={(props) => {
        handleAuthentication(props);
        return <Callback {...props} />
      }}/>
    </div>
  </Router>
);

export default Routes;
