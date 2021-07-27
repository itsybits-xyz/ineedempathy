import React, { FC, useState, useEffect } from 'react';
import { BACKEND_URL } from '../config';
import { isEmptyValue, getCard } from '../utils';
import { Hidden } from '../components';
import { CardHeader } from './card-header';
import { CardComments } from './card-comments';
import { Card } from '../schemas';

export interface CardPageProps {
  match: {
    params: {
      type: string
      name: string
    }
  }
};

export const CardPage: FC<CardPageProps> = (props: CardPageProps) => {
  const { name } = props.match.params;
  const [ error, setError ] = useState();
  const [ card, setCard ] = useState<Card>({} as Card);

  useEffect(() => {
    getCard(name).then((data) => {
      setCard(data);
    }).catch((er) => {
      setError(er);
    });
  }, [name]);

  if (!isEmptyValue(error)) {
    return (
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={error} />
      </>
    );
  }

  return card.name ? (
    <>
      <CardHeader card={card} />
      <CardComments card={card} />
    </>
  ) : (
    <p>Loading...</p>
  );
};
