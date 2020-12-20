import React, { FC } from 'react';
import { Switch, Route } from 'react-router-dom';
import { useHistory } from 'react-router';

import {
  Home,
} from './views';
import { NavBar, SideBar } from './components';

export const Routes: FC = () => {
  const history = useHistory();

  return (
    <Switch>
      <div className="wrapper">
        <SideBar />
        <div className="main-panel">
          <NavBar />
          <Route exact path="/" component={Home} />
        </div>
      </div>
    </Switch>
  );
};
