import useSound from 'use-sound';

import nudgePersonSound from '../sound/rising-pops.mp3';
import toggleCardSound from '../sound/toggle-card.mp3';
import matchSound from '../sound/match.wav';

export function PlaySound() {
  const [ playMatchSound ] = useSound(matchSound);
  const [ playToggleSound ] = useSound(toggleCardSound);
  const [ playNudgeSound ] = useSound(nudgePersonSound);

  return {
    playMatch: playMatchSound,
    playToggle: playToggleSound,
    playNudge: playNudgeSound,
  };
};
