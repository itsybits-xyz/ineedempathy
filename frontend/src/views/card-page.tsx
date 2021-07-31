import React, { FC, useState, useEffect } from 'react';
import { getCard } from '../utils';
import { ClickSound, Hidden } from '../components';
import { CardHeader } from './card-header';
import { CardComments } from './card-comments';
import { Card } from '../schemas';
import { Link } from 'react-router-dom';
import { Button, Row } from 'react-bootstrap';

export interface CardPageProps {
  match: {
    params: {
      type: string
      name: string
    }
  }
};

export const CardPage: FC<CardPageProps> = (props: CardPageProps) => {
  const { name, type } = props.match.params;
  const [ error, setError ] = useState();
  const [ card, setCard ] = useState<Card>({} as Card);

  useEffect(() => {
    getCard(name).then((data) => {
      setCard(data);
    }).catch((er) => {
      setError(er);
    });
  }, [name]);

  if (error) {
    return (
      <Hidden error={error} />
    );
  }

  return card.name ? (
    <>
      <Row className="justify-content-sm-center">
        <ClickSound>
          <Link to={type === 'feeling' ? '/feelings' : '/needs'}>
            <Button>Go Back</Button>
          </Link>
        </ClickSound>
      </Row>
      <CardHeader card={card} />
      <CardComments card={card} />
    </>
  ) : (
    <p role="alert">Loading...</p>
  );
};
