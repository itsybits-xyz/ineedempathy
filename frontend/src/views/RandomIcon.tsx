import React, { FC, useState, useEffect } from 'react';
const IconList = require('react-icons/md');

export interface RandomIconProps {
  string: string
  size: number
}

export const RandomIcon: FC<RandomIconProps> = (props: RandomIconProps) => {
  const [key, setKey] = useState<string>();
  const {string, size} = props;

  useEffect(() => {
    const keys = Object.keys(IconList);
    const count = keys.length;
    const key = parseInt(string.toLowerCase().replace(/[^a-z0-9]/g, ''), 36) % count;
    setKey(keys[key]);
  }, [string]);

  if (!key) {
    return null;
  }

  const Ikon = IconList[key];
  return <Ikon size={size} />
};
