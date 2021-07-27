import React, { FC, useState } from 'react';

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
        { hidden ? (
          <button onClick={() => setHidden(false) }>Show</button>
        ) : (
          <>
            <button onClick={() => setHidden(true) }>Hide</button>
            { props.error && (
              <>
                <p>Message: {props.error.message}</p>
                <Hidden>
                  <h3>Stack</h3>
                  <p>{props.error.stack}</p>
                </Hidden>
              </>
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
