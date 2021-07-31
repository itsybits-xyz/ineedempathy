import { FC } from 'react';
import { PlaySound } from '.';

export interface ClickSoundProps {
  children?: any;
}

export const ClickSound: FC<ClickSoundProps> = (props: ClickSoundProps) => {
  const { playToggle } = PlaySound();
  return (
    <span onClick={() => playToggle() }>
        {props.children}
    </span>
  );
};
