import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { Card } from 'react-bootstrap';
import { Hidden } from '.';
import { MdInfoOutline, MdRemoveCircleOutline, MdLibraryAdd } from 'react-icons/md';

export interface GameCardProps {
  card: CardSchema;
  handleClick: () => void;
  size?: string;
  onList: boolean;
};

export const GameCard: FC<GameCardProps> = (props: GameCardProps) => {
  const { size, card, handleClick, onList } = props;
  const [ error, setError ] = useState(false);
  let cardWidth;
  let toggleSize;
  switch (size) {
    case 'sm':
      cardWidth = '5rem'
      toggleSize = 15
      break;
    case 'md':
      cardWidth = '7rem'
      toggleSize = 25
      break;
    case 'lg':
    default:
      cardWidth = '10rem';
      toggleSize = 36
  }
  if (error) {
    return <Hidden error={error} />
  }
  return (
    <Card style={{ width: cardWidth }}>
      <div className="kard">
        <Card.Img
          alt={card.displayName}
          variant="top"
          onError={(er: any) => setError(er)}
          src={ BACKEND_URL + card.image.md } />
        <div className={"ikon " + size}>
          <MdInfoOutline size={toggleSize} />
        </div>
      </div>
      <Card.Body
        onClick={handleClick}
        className={onList ? 'on-list' : 'off-list'}>
        <Card.Title className={size}>{card.displayName}</Card.Title>
        <Card.Title>
          <MdRemoveCircleOutline className="remove" size={toggleSize} />
          <MdLibraryAdd className="add" size={toggleSize} />
        </Card.Title>
      </Card.Body>
    </Card>
  );
};
