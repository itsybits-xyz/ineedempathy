import React, { FC } from 'react';

export interface NavBarProps {
  handleClick: () => void,
};

export const NavBar: FC<NavBarProps> = (props: NavBarProps) => {
  const { handleClick } = props;
  return (
    <>
      <nav className="navbar navbar-transparent navbar-absolute fixed-top-right">
        <div className="pos-top-right container-fluid">
          <button onClick={handleClick} className="navbar-toggler" type="button" data-toggle="collapse" aria-controls="navigation-index" aria-expanded="false" aria-label="Toggle navigation">
            <span className="sr-only">Toggle navigation</span>
            <span className="navbar-toggler-icon icon-bar"></span>
            <span className="navbar-toggler-icon icon-bar"></span>
            <span className="navbar-toggler-icon icon-bar"></span>
          </button>
        </div>
      </nav>
    </>
  );
};
