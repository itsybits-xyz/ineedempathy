import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { Card } from 'react-bootstrap';
import { Hidden } from '.';

export interface GameCardProps {
  card: CardSchema;
  handleClick: () => void;
};

export const GameCard: FC<GameCardProps> = (props: GameCardProps) => {
  const { card, handleClick } = props;
  const [ error, setError ] = useState(false);
  if (error) {
    return <Hidden error={error} />
  }
  return (
    <Card onClick={handleClick} style={{ width: '10rem' }}>
      <Card.Img
        alt={card.name}
        variant="top"
        onError={(er: any) => setError(er)}
        src={ BACKEND_URL + card.textUrl } />
      <Card.Body>
        <Card.Title>{card.name}</Card.Title>
      </Card.Body>
    </Card>
  );
};
