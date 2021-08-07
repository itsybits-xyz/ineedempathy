import React, { FC } from 'react';
import { NavLink } from 'react-router-dom';
import { MdWbSunny, MdDashboard, MdLayers, MdFavorite } from 'react-icons/md';
import { VolumeControl } from "../components";
import { ClickSound } from '.';

export interface SideBarProps {
  handleClick: () => void,
};


export const SideBar: FC<SideBarProps> = (props: SideBarProps) => {
  const { handleClick } = props;
  const isActiveFor = (navLinkMatch:RegExp) => {
    return (match:any, location:any) => {
      return location?.pathname?.match(navLinkMatch);
    };
  };
  return (
    <>
      <div
        className="sidebar"
        data-color="purple"
        data-background-color="white"
        onClick={handleClick}
      >
        <div className="logo">
          <a href="http://ineedempathy.com" className="simple-text logo-normal">
            I NEED EMPATHY
          </a>
        </div>
        <div className="sidebar-wrapper">
          <ul className="nav">
            <li className="nav-item">
              <ClickSound>
                <NavLink to="/" exact={true} className="nav-link" activeClassName="active">
                  <MdDashboard size={24}/>
                  <p>
                    Start
                  </p>
                </NavLink>
              </ClickSound>
            </li>
            <li className="nav-item">
              <ClickSound>
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
              </ClickSound>
            </li>
            <li className="nav-item">
              <ClickSound>
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
              </ClickSound>
            </li>
            <li className="nav-item">
              <ClickSound>
                <NavLink to="/about" className="nav-link" activeClassName="active">
                  <MdLayers size={24}/>
                  <p>
                    About
                  </p>
                </NavLink>
              </ClickSound>
            </li>
          </ul>
          <VolumeControl />
        </div>
      </div>
    </>
  );
};
