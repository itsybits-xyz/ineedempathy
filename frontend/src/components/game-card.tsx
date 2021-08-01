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
  let width;
  switch (size) {
    case 'sm':
        width = '5rem'
      break;
    case 'md':
      width = '7rem'
      break;
    case 'lg':
    default:
      width = '10rem';
  }
  if (error) {
    return <Hidden error={error} />
  }
  return (
    <Card style={{ width: width }}>
      <div className="kard">
        <Card.Img
          alt={card.name}
          variant="top"
          onError={(er: any) => setError(er)}
          src={ BACKEND_URL + card.textUrl } />
        <div className="ikon">
          <MdInfoOutline size={36} />
        </div>
      </div>
      <Card.Body
        onClick={handleClick}
        className={onList ? 'on-list' : 'off-list'}>
        <Card.Title className={size}>{card.name}</Card.Title>
        <Card.Title>
          <MdRemoveCircleOutline className="remove" size={36} />
          <MdLibraryAdd className="add" size={36} />
        </Card.Title>
      </Card.Body>
    </Card>
  );
};
