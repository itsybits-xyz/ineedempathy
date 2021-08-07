import React, { FC, useState } from "react";
import useSound from 'use-sound';
import { MdVolumeDown, MdVolumeUp } from 'react-icons/md';

import nudgePersonSound from '../sound/rising-pops.mp3';
import toggleCardSound from '../sound/toggle-card.mp3';
import matchSound from '../sound/match.wav';
const VOLUME = 'PlaySound.volume';
const MAX_VOLUME = 100;
const MIN_VOLUME = 0;
const INC_VOLUME = 10;
const DEF_VOLUME = 70;
const MUL_VOLUME = 0.01;
const getSavedVolume = ():number => {
  const raw = parseFloat(localStorage.getItem(VOLUME))
  if (raw === 0) {
    return raw;
  }
  return raw || DEF_VOLUME;
};

export function PlaySound() {
  const [ _tick, setTick ] = useState(0);
  const [ playMatchSound, { sound: howlerMatch } ] = useSound(matchSound);
  const [ playToggleSound, { sound: howlerToggle } ] = useSound(toggleCardSound);
  const [ playNudgeSound, { sound: howlerNudge } ] = useSound(nudgePersonSound);

  const tick = () => {
    setTick(_tick > 100 ? 0 : _tick + 1);
  };

  return {
    playMatch: () => {
      howlerMatch?.volume(getSavedVolume() * MUL_VOLUME)
      playMatchSound();
    },
    playToggle: () => {
      howlerToggle?.volume(getSavedVolume() * MUL_VOLUME)
      playToggleSound()
    },
    playNudge: () => {
      howlerNudge?.volume(getSavedVolume() * MUL_VOLUME)
      playNudgeSound();
    },
    volume: {
      value: getSavedVolume,
      set: (value:number) => {
        localStorage.setItem(VOLUME, String(value));
        tick();
      },
      up: () => {
        localStorage.setItem(VOLUME, String(Math.min(
          MAX_VOLUME,
          getSavedVolume() + INC_VOLUME
        )));
        tick();
      },
      down: () => {
        localStorage.setItem(VOLUME, String(Math.max(
          MIN_VOLUME,
          getSavedVolume() - INC_VOLUME
        )));
        tick();
      },
    }
  };
};

export const VolumeEl: FC<VolumeElProps> = (props: VolumeElProps) => {
  const { value, set, up, down, onChange } = props;
  return (
    <>
      <MdVolumeDown onClick={() => { down(); onChange(); }} />
      <input
        type="range"
        min={MIN_VOLUME}
        max={MAX_VOLUME}
        onChange={(ev) => {
          set(parseInt(ev.target.value));
          onChange();
        }}
        value={value()} />
      <MdVolumeUp onClick={() => { up(); onChange(); }} />
    </>
  );
};

export interface VolumeElProps {
  onChange: () => void;
  value: () => number;
  set: () => void;
  up: () => void;
  down: () => void;
};

PlaySound.VolumeEl = VolumeEl;
