import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { Card } from 'react-bootstrap';
import { Hidden } from '.';
import { MdInfoOutline, MdRemoveCircleOutline, MdLibraryAdd } from 'react-icons/md';

export interface GameCardProps {
  card: CardSchema;
  handleClick: () => void;
  handleInfo: () => void;
  size?: string;
  onList: boolean;
};

export const GameCard: FC<GameCardProps> = (props: GameCardProps) => {
  const { size, card, handleInfo, handleClick, onList } = props;
  const [ error, setError ] = useState(false);
  let toggleSize;
  switch (size) {
    case 'sm':
      toggleSize = 15
      break;
    case 'md':
      toggleSize = 25
      break;
    case 'lg':
    default:
      toggleSize = 36
  }
  if (error) {
    return <Hidden error={error} />
  }
  return (
    <Card className={`game-card ${size}`}>
      <div
        role="link"
        title={(
          onList ? (
            `Click to remove the card ${card.displayName} to your list.`
          ) : (
            `Click to add the card ${card.displayName} to your list.`
          )
        )}
        tabIndex={0}
        onClick={handleClick}
        className={onList ? 'kard on-list' : 'kard off-list'}>
        <Card.Img
          alt={card.displayName}
          variant="top"
          onError={(er: any) => setError(er)}
          src={ BACKEND_URL + card.image.md } />
        <div className={"ikon " + size}>
          <MdRemoveCircleOutline className="remove" size={toggleSize} />
          <MdLibraryAdd className="add" size={toggleSize} />
        </div>
      </div>
      <Card.Body
        role="link"
        title={`Click to get more information on ${card.displayName}`}
        tabIndex={0}
        onClick={handleInfo}>
        <Card.Title className={size}>{card.displayName}</Card.Title>
        <Card.Title>
          <MdInfoOutline size={toggleSize} />
        </Card.Title>
      </Card.Body>
    </Card>
  );
};
