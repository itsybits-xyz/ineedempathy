import useSound from 'use-sound';
import { useState, useEffect } from "react";

import nudgePersonSound from '../sound/rising-pops.mp3';
import toggleCardSound from '../sound/toggle-card.mp3';
import matchSound from '../sound/match.wav';

const VOLUME = 'PlaySound.volume';
const MAX_VOLUME = 100;
const MIN_VOLUME = 0;
const INC_VOLUME = 10;
const DEF_VOLUME = 70;
const MUL_VOLUME = 0.01;
const getSavedVolume = () => {
  const raw = parseFloat(localStorage.getItem(VOLUME))
  if (raw === 0) {
    return raw;
  }
  return raw || DEF_VOLUME;
};

export function PlaySound() {
  const [ tick, setTick ] = useState(0);
  const [ playMatchSound, { sound: howlerMatch } ] = useSound(matchSound);
  const [ playToggleSound, { sound: howlerToggle } ] = useSound(toggleCardSound);
  const [ playNudgeSound, { sound: howlerNudge } ] = useSound(nudgePersonSound);

  return {
    playMatch: () => {
      howlerMatch.volume(getSavedVolume() * MUL_VOLUME)
      playMatchSound();
    },
    playToggle: () => {
      howlerToggle.volume(getSavedVolume() * MUL_VOLUME)
      playToggleSound()
    },
    playNudge: () => {
      howlerNudge.volume(getSavedVolume() * MUL_VOLUME)
      playNudgeSound();
    },
    volume: {
      value: getSavedVolume,
      up: () => {
        localStorage.setItem(VOLUME, String(Math.min(
          MAX_VOLUME,
          getSavedVolume() + INC_VOLUME
        )));
        setTick(tick > 100 ? 0 : tick + 1);
      },
      down: () => {
        localStorage.setItem(VOLUME, String(Math.max(
          MIN_VOLUME,
          getSavedVolume() - INC_VOLUME
        )));
        setTick(tick > 100 ? 0 : tick + 1);
      },
    }
  };
};
