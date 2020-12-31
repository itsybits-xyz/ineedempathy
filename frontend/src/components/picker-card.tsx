import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card } from '../schemas';

export interface PickerCardProps {
  card: Card;
};

export const PickerCard: FC<PickerCardProps> = (props: PickerCardProps) => {
  return (
    <img alt={props.card.name} width={200} src={BACKEND_URL + props.card.textUrl} />
  );
};
