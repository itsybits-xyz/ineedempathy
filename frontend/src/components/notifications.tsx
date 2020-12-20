import React, { FC, useState } from 'react';
import classNames from "classnames";
import {MdNotifications} from "react-icons/md";

export const Notifications: FC = () => {
  const [ showDropDown, setShowDropDown ] = useState<boolean>(false);
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    setShowDropDown(!showDropDown);
  }
  const liClasses = classNames({"nav-item": true, dropdown: true, show: showDropDown})
  const dropDownClasses = classNames({"dropdown-menu": true, "dropdown-menu-right":true, show: showDropDown})
  return (
    <li className={liClasses}>
      <a className="nav-link" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" onClick={handleClick}>
        <MdNotifications size={32}/>
        <span className="notification">5</span>
        <p className="d-lg-none d-md-block">
          Some Actions
        </p>
        <div className="ripple-container"></div></a>
      <div className={dropDownClasses}>
        <a className="dropdown-item" href="#">Mike John responded to your email</a>
        <a className="dropdown-item" href="#">You have 5 new tasks</a>
        <a className="dropdown-item" href="#">You're now friend with Andrew</a>
        <a className="dropdown-item" href="#">Another Notification</a>
        <a className="dropdown-item" href="#">Another One</a>
      </div>
    </li>
  )
}
