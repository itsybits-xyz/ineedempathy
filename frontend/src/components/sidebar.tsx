import React, { FC } from 'react';
import {MdDashboard, MdPerson} from 'react-icons/md';

export const SideBar: FC = () => {
  return (
    <>
      <div
        className="sidebar"
        data-color="purple"
        data-background-color="white"
        data-image="../assets/img/sidebar-1.jpg"
      >
        <div className="logo">
          <a href="http://ineedempathy.com" className="simple-text logo-normal">
            iNeedEmpathy
          </a>
        </div>
        <div className="sidebar-wrapper">
          <ul className="nav">
            <li className="nav-item active  ">
              <a className="nav-link" href="/trips">
                <p>
                  <MdDashboard size={24}/>
                  Game
                </p>
              </a>
            </li>
            <li className="nav-item ">
              <a className="nav-link" href="/user">
                <p>
                  <MdPerson size={24}/>
                  User Profile
                </p>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};
