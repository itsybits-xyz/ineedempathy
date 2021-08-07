import React, { FC, useState } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import {
  Home,
  Room,
  RoomProps,
  CardPageProps,
  About,
  Inventory,
  CardPage,
} from './views';
import { NavBar, SideBar } from './components';

export const Routes: FC = () => {
  const [ navOpen, setNavOpen ] = useState(false);
  return (
    <BrowserRouter>
      <Switch></Switch>
      <div className={navOpen ? "nav-open wrapper" : "wrapper"}>
        <SideBar handleClick={() => setNavOpen(false) } />
        <div className="main-panel">
          <NavBar handleClick={() => { setNavOpen(!navOpen); }} />
          <Route exact path="/" component={Home} />
          <Route path="/room/:name" component={(props: RoomProps) => <Room {...props} /> } />
          <Route path="/about" component={About} />
          <Route path="/:type(feeling|need)/:name" component={(props: CardPageProps) => {
            const newProps = Object.assign({}, props, {
              backButton: true,
            });
            return <CardPage {...newProps} />;
          }} />
          <Route path="/:type(feelings|needs)" component={Inventory} />
        </div>
      </div>
    </BrowserRouter>
  );
};
