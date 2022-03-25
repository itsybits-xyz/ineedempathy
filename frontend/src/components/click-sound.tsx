import { FC } from 'react';
import { PlaySound } from '.';

export interface ClickSoundProps {
  children?: any;
  onClick?: () => void;
}

export const ClickSound: FC<ClickSoundProps> = (props: ClickSoundProps) => {
  const { playToggle } = PlaySound();

  const handleOnClick = () => {
    return () => {
      playToggle();
      if (props.onClick) props.onClick();
    }
  }

  return (
    <span onClick={handleOnClick}>
        {props.children}
    </span>
  );
};
