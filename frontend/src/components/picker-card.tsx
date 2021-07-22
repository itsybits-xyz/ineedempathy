import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card } from '../schemas';

export interface PickerCardProps {
  card: Card;
};

export const PickerCard: FC<PickerCardProps> = (props: PickerCardProps) => {
  const card: Card = props.card;
  return (
    <a className="fn-card" href={`/${card.type}/${card.name}`}>
      <img alt={card.name} width={200} src={BACKEND_URL + card.textUrl} />
    </a>
  );
};
