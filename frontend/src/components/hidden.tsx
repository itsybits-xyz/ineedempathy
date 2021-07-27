import React, { FC, useState } from 'react';
import { MdWarning } from 'react-icons/md';

export interface HiddenProps {
  error?: any;
  children?: any;
  message?: string;
}

/**
 * <Hidden error={new Error('meow')} />
 * <Hidden message={"Hello world"} />
 * <Hidden><p>Meow</p></Hidden>
 **/
export const Hidden: FC<HiddenProps> = (props: HiddenProps) => {
  const [hidden, setHidden] = useState<boolean>(true);
  return (
    <>
      <div role="alert" className="hidden">
        <h3>
          <MdWarning size={36}/>
          <p>An unexpected error occured.</p>
        </h3>
        { hidden ? (
          <button onClick={() => setHidden(false) }>Show</button>
        ) : (
          <>
            <button onClick={() => setHidden(true) }>Hide</button>
            { props.error && (
              <div>
                <h4>Error Details</h4>
                <strong>Message</strong>
                <p>{props.error.message}</p>
                <strong>Stack</strong>
                <p>{props.error.stack}</p>
              </div>
            ) }
            { props.children && (
              <p>
                {props.children}
              </p>
            ) }
            { props.message && (
              <p>
                { props.message }
              </p>
            ) }
          </>
        )}
      </div>
    </>
  );
};
