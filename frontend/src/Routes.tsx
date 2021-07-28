import React, { FC } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import { useHistory } from 'react-router';

import {
  Home,
  Room,
  RoomProps,
  CardPageProps,
  About,
  Inventory,
  CardPage,
} from './views';
import { SideBar } from './components';

export const Routes: FC = () => {
  const history = useHistory();
  const currentPath = history?.location?.pathname || '';

  return (
    <BrowserRouter>
      <Switch></Switch>
      <div className="wrapper">
        <SideBar currentPath={currentPath} />
        <div className="main-panel">
          <Route exact path="/" component={Home} />
          <Route path="/room/:name" component={(props: RoomProps) => <Room {...props} /> } />
          <Route path="/about" component={About} />
          <Route path="/:type(feeling|need)/:name" component={(props: CardPageProps) => <CardPage {...props} /> } />
          <Route path="/:type(feelings|needs)" component={Inventory} />
        </div>
      </div>
    </BrowserRouter>
  );
};
