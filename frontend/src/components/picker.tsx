import React, { FC, useState } from 'react';
import { ButtonGroup, Button, Container, Col, Row } from 'react-bootstrap';
import { getCards } from '../utils/api';
import { useAsync } from 'react-async';
import { PlaySound, PickerCard, Hidden } from './';
import { CardLevel, Card } from '../schemas';

export interface PickerProps {
  type?: string;
  name?: string;
};

const defaultProps: PickerProps = {
    type: 'needs',
};

export const Picker: FC<PickerProps> = (props: PickerProps) => {
  const { playToggle } = PlaySound();
  const { data, error, isPending } = useAsync(getCards);
  const [ level, _setLevel ] = useState<CardLevel>(CardLevel.all);

  const setLevel = (newLevel: CardLevel) => {
    playToggle();
    return _setLevel(newLevel);
  };

  const isCardLevel = (lookLevel: CardLevel, success: any, fail: any):any => {
    return lookLevel === level ? success : fail;
  };

  if (error) {
    return (
      <Hidden error={error} />
    );
  }

  if (isPending || !data) {
    return (
      <div className="content">
        Loading...
      </div>
    );
  }

  const filterType = props.type === 'needs' ? 'need' : 'feeling';
  const cards = data.filter((card: Card) => {
    return card.type === filterType;
  }).filter((card: Card) => {
      if (level === CardLevel.all) return true;
      return card.level <= level;
  }).sort((card1: Card, card2: Card) => {
    if (Math.floor(Math.random() * 1000) % 2 === 0) return 1;
    if (Math.floor(Math.random() * 1000) % 2 === 0) return -1;
    return 0;
  });

  return (
    <div className="content fn-cards">
      <Container fluid>
        <Row>
          <ButtonGroup aria-label="Basic example">
            <Button
              onClick={() => setLevel(CardLevel.intro) }
              variant={isCardLevel(CardLevel.intro, "primary", "secondary")}>
              Intro
            </Button>
            <Button
              onClick={() => setLevel(CardLevel.beginner) }
              variant={isCardLevel(CardLevel.beginner, "primary", "secondary")}>
              Beginner
            </Button>
            <Button
              onClick={() => setLevel(CardLevel.intermediate) }
              variant={isCardLevel(CardLevel.intermediate, "primary", "secondary")}>
              Intermediate
            </Button>
            <Button
              onClick={() => setLevel(CardLevel.all) }
              variant={isCardLevel(CardLevel.all, "primary", "secondary")}>
              All
            </Button>
          </ButtonGroup>
        </Row>
        <Row>
          { cards.map((card) => {
            return (
              <Col key={card.id}>
                <PickerCard card={ card } />
              </Col>
            );
          }) }
        </Row>
      </Container>
    </div>
  );
};

Picker.defaultProps = defaultProps;
