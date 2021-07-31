import { FC } from 'react';
import useSound from 'use-sound';

import toggleCardSound from '../sound/toggle-card.mp3';

export interface ClickSoundProps {
  children?: any;
}

export const ClickSound: FC<ClickSoundProps> = (props: ClickSoundProps) => {
  const [playSound] = useSound(toggleCardSound);
  return (
    <span onClick={() => playSound() }>
        {props.children}
    </span>
  );
};
