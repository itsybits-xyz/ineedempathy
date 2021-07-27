import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card } from '../schemas';

export interface CardHeaderProps {
  card: Card,
};

export const CardHeader: FC<CardHeaderProps> = (props: CardHeaderProps) => {
  const { card } = props;

  if (!card.name) {
    return (
      <>
        <div className="content">
          Loading...
        </div>
      </>
    );
  }

  return (
    <>
        <img alt={card.name} width={200} src={BACKEND_URL + card.textUrl} />
    </>
  );
};
