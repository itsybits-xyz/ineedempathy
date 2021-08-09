import React, { FC, useState } from 'react';
import { Alert, Dropdown, Container, Col, Form, Row } from 'react-bootstrap';
import { displayLevel, getCards } from '../utils';
import { useAsync } from 'react-async';
import { PlaySound, PickerCard, Hidden } from './';
import { CardLevel, Card } from '../schemas';
import fuzzyfind from 'fuzzyfind';

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
  const [ query, setQuery ] = useState<string>('');

  const setLevel = (newLevel: CardLevel) => {
    playToggle();
    return _setLevel(newLevel);
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
  const cards = fuzzyfind(query, data, {
    accessor: (card: Card) => {
      return `${card.name} ${card.displayName} ${card.definition}`;
    },
  }).filter((card: Card) => {
    return card.type === filterType;
  }).filter((card: Card) => {
    if (level === CardLevel.all) return true;
    return card.level <= level;
  });

  return (
    <div className="content fn-cards">
      <Container fluid>
        <Row>
          <Dropdown>
            <Dropdown.Toggle variant="success">
              {displayLevel(level)}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item
                active={level === CardLevel.intro}
                onClick={() => setLevel(CardLevel.intro)}>
                {displayLevel(CardLevel.intro)}
              </Dropdown.Item>
              <Dropdown.Item
                active={level === CardLevel.beginner}
                onClick={() => setLevel(CardLevel.beginner)}>
                {displayLevel(CardLevel.beginner)}
              </Dropdown.Item>
              <Dropdown.Item
                active={level === CardLevel.intermediate}
                onClick={() => setLevel(CardLevel.intermediate)}>
                {displayLevel(CardLevel.intermediate)}
              </Dropdown.Item>
              <Dropdown.Item
                active={level === CardLevel.all}
                onClick={() => setLevel(CardLevel.all)}>
                {displayLevel(CardLevel.all)}
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Row>
        <Row>
          <Form.Control
            size='lg'
            value={query}
            onChange={(ev) => setQuery(ev.target.value)}
            type="input"
            placeholder="Search..." />
        </Row>
        <Row>
          { cards.length === 0 ? (
            <Alert variant="light">
              No cards were found. Try expanding your filters or removing your search term.
            </Alert>
          ) : (
            cards.map((card: Card) => {
              return (
                <Col key={card.id}>
                  <PickerCard card={ card } />
                </Col>
              );
            })
          )}
        </Row>
      </Container>
    </div>
  );
};

Picker.defaultProps = defaultProps;
