import React from 'react';
import { Route, Router } from 'react-router-dom';
import Home from './Home';
import ANumber from './A_Number_Attemps/Alarm1';
import AMotion from './A_Motion/Alarm1';
import ADoor from './A_Door/Alarm1';
import ABattery from './A_Battery/Alarm1';
import AHub from './A_Hub/Alarm1';
import ALock from './A_Lock/Alarm1';
import Callback from './Callback';
import Auth from './auth';
import history from './history';

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}

const Routes = () => (
  <Router history={history} component={Home}>
    <div style={{width: '100%', height: '100%'}}>
      <Route exact path="/" render={(props) => <Home auth={auth} {...props} />} />
      <Route path="/home" render={(props) => <Home auth={auth} {...props} />} />
      <Route path="/number" render={(props) => <ANumber auth={auth} {...props} />} />
      <Route path="/motion" render={(props) => <AMotion auth={auth} {...props} />} />
      <Route path="/door" render={(props) => <ADoor auth={auth} {...props} />} />
      <Route path="/battery" render={(props) => <ABattery auth={auth} {...props} />} />
      <Route path="/hub" render={(props) => <AHub auth={auth} {...props} />} />
      <Route path="/lock" render={(props) => <ALock auth={auth} {...props} />} />
      <Route path="/callback" render={(props) => {
        handleAuthentication(props);
        return <Callback {...props} />
      }}/>
    </div>
  </Router>
);

export default Routes;
