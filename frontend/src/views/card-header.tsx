import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card } from '../schemas';
import { MdWarning } from 'react-icons/md';

export interface CardHeaderProps {
  card: Card,
};

export const CardHeader: FC<CardHeaderProps> = (props: CardHeaderProps) => {
  const { card } = props;
  const [ error, setError ] = useState();

  return error ? (
    <div role="alert">
      <MdWarning size={24}/>
      <p>Image failed to load</p>
    </div>
  ) : (
    <img
      onError={(er: any) => setError(er)}
      alt={card.name}
      width={350}
      src={BACKEND_URL + card.textUrl} />
  );
};
