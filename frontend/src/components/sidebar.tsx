import React, { FC } from 'react';
import { NavLink } from 'react-router-dom';
import { MdExtension, MdWbSunny, MdDashboard, MdLayers, MdFavorite } from 'react-icons/md';

export const SideBar: FC = () => {
  const isActiveFor = (navLinkMatch) => {
    return (match, location) => {
      return location?.pathname?.match(navLinkMatch);
    };
  };
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
            <li className="nav-item">
              <NavLink to="/" exact={true} className="nav-link" activeClassName="active">
                <MdDashboard size={24}/>
                <p>
                  Start
                </p>
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink
                to="/feelings"
                className="nav-link"
                isActive={isActiveFor(/^\/feeling.*$/)}
                activeClassName="active">
                <MdFavorite size={24}/>
                <p>
                  Feelings
                </p>
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink
                to="/needs"
                className="nav-link"
                isActive={isActiveFor(/^\/need.*$/)}
                activeClassName="active">
                <MdWbSunny size={24}/>
                <p>
                  Needs
                </p>
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/about" className="nav-link" activeClassName="active">
                <MdLayers size={24}/>
                <p>
                  About
                </p>
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
};
