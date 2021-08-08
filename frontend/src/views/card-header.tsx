import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { MdWarning } from 'react-icons/md';
import { Card, Row } from 'react-bootstrap';

export interface CardHeaderProps {
  card: CardSchema,
};

export const CardHeader: FC<CardHeaderProps> = (props: CardHeaderProps) => {
  const { card } = props;
  const [ error, setError ] = useState(false);

  const getDomain = (url: string): string => {
    const urlObj = new URL('https://www.lexico.com/en/definition/angry');
    return urlObj.hostname;
  };

  return error ? (
    <div role="alert">
      <MdWarning size={24}/>
      <p>Image failed to load</p>
    </div>
  ) : (
    <Row className="justify-content-md-center">
      <Card>
        <Card.Img
          alt={card.displayName}
          variant="top"
          onError={(er: any) => setError(er)}
          src={ BACKEND_URL + card.image.lg } />
        <Card.Body>
          <Card.Title>{card.displayName}</Card.Title>
          <Card.Text>
            {card.definition}
          </Card.Text>
          <Card.Text>
            Source:
            <a rel="noreferrer" target="_blank" href={card.definitionSource}>
              {getDomain(card.definitionSource)}
            </a>
          </Card.Text>
        </Card.Body>
      </Card>
    </Row>
  );
};
