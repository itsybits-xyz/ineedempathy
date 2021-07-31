import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card as CardSchema } from '../schemas';
import { MdWarning } from 'react-icons/md';
import { Card, Container, Row } from 'react-bootstrap';

export interface CardHeaderProps {
  card: CardSchema,
};

export const CardHeader: FC<CardHeaderProps> = (props: CardHeaderProps) => {
  const { card } = props;
  const [ error, setError ] = useState(false);

  return error ? (
    <div role="alert">
      <MdWarning size={24}/>
      <p>Image failed to load</p>
    </div>
  ) : (
    <Container fluid>
      <Row className="justify-content-md-center">
        <Card style={{ width: '35rem' }}>
          <Card.Img
            alt={card.displayName}
            variant="top"
            onError={(er: any) => setError(er)}
            src={ BACKEND_URL + card.textUrl } />
          <Card.Body>
            <Card.Title>{card.displayName}</Card.Title>
            <Card.Text>
              {card.definition}
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>
    </Container>
  );
};
