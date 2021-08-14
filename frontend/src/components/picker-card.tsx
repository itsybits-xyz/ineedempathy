import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { ClickSound } from '.';

export interface PickerCardProps {
  card: CardSchema;
};

export const PickerCard: FC<PickerCardProps> = (props: PickerCardProps) => {
  const card: CardSchema = props.card;
  return (
    <Link
      role="link"
      tabIndex={0}
      title={`${card.displayName} - ${card.definition}`}
      to={`/${card.type}/${card.name}`}>
      <ClickSound>
        <Card>
          <Card.Img
            alt={card.name}
            variant="top"
            src={ BACKEND_URL + card.image.md } />
          <Card.Body>
            <Card.Title>{card.displayName}</Card.Title>
          </Card.Body>
        </Card>
      </ClickSound>
    </Link>
  );
};
