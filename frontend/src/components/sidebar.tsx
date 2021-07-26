import React, { FC } from 'react';
import { MdExtension, MdWbSunny, MdDashboard, MdLayers, MdFavorite } from 'react-icons/md';

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
            I NEED EMPATHY
          </a>
        </div>
        <div className="sidebar-wrapper">
          <ul className="nav">
            <li className="nav-item active">
              <a className="nav-link" href="/">
                <MdDashboard size={24}/>
                <p>
                  Play
                </p>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/">
                <MdExtension size={24}/>
                <p>
                  How to Play
                </p>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/feelings">
                <MdFavorite size={24}/>
                <p>
                  Feelings
                </p>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/needs">
                <MdWbSunny size={24}/>
                <p>
                  Needs
                </p>
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/about">
                <MdLayers size={24}/>
                <p>
                  About
                </p>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};
