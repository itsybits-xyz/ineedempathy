import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Container, Col, Row } from 'react-bootstrap';
import { getCards } from '../utils/api';
import { useAsync } from 'react-async';
import { Hidden } from '../components';
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
  const { data, error, isPending } = useAsync(getCards);

  if (error) {
    return (
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={error} />
      </>
    );
  }

  if (isPending || !data) {
    return (
      <>
        <div className="content">
          Loading...
        </div>
      </>
    );
  }

  const cards: Card[] = data.filter((card: Card) => {
    return card.name === name;
  });

  const card: Card = cards[0];

  if (!card) {
    return (
      <>
        <div className="content">
          Card not found.
        </div>
      </>
    );
  }

  return (
    <>
      <img alt={card.name} width={200} src={BACKEND_URL + card.textUrl} />
    </>
  );

};
