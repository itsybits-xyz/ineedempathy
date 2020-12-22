import React, { FC } from 'react';
import {MdSearch} from "react-icons/md";

export const Search: FC = () => {
  return (
    <>
      <form className="navbar-form">
        <span className="bmd-form-group">
          <div className="input-group no-border">
            <input
              type="text"
              className="form-control"
              placeholder="Search..."
            />
            <button type="submit" className="btn btn-white btn-round btn-just-icon">
              <MdSearch size={24}/>
              <div className="ripple-container"></div>
            </button>
          </div>
        </span>
      </form>
    </>
  );
};
