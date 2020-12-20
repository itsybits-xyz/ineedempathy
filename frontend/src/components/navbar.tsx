import React, { FC } from 'react';
import {Search} from './search';
import {Notifications} from './notifications';
import {MdPerson} from 'react-icons/md';

export const NavBar: FC = () => {
  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-transparent navbar-absolute fixed-top ">
        <div className="container-fluid">
          <div className="collapse navbar-collapse justify-content-end">
            <Search />
            <ul className="navbar-nav">
              <Notifications />
              <li className="nav-item dropdown">
                <a className="nav-link" href="javascript:;" id="navbarDropdownProfile" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <MdPerson size={32}/>
                  <p className="d-lg-none d-md-block">
                    Account
                  </p>
                  <div className="ripple-container"></div></a>
                <div className="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownProfile">
                  <a className="dropdown-item" href="#">Profile</a>
                  <a className="dropdown-item" href="#">Settings</a>
                  <div className="dropdown-divider"></div>
                  <a className="dropdown-item" href="#">Log out</a>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </>
  )
}
