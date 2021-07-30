import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

export interface GameCardProps {
  card: CardSchema;
  handleClick: () => void;
};

export const GameCard: FC<GameCardProps> = (props: GameCardProps) => {
  const { card, handleClick } = props;
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
