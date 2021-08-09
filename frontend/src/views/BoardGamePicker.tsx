import React, { FC, useState } from "react";
import { Alert, Button, Col, Dropdown, Form, Row } from 'react-bootstrap';
import { PlaySound, GameCard } from "../components";
import { CardLevel, CardType, Card } from "../schemas";
import { displayLevel } from '../utils';
import fuzzyfind from 'fuzzyfind';

export interface BoardGamePickerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  onList: (card: Card) => boolean;
  setSelectedCard: (card: Card|null) => void;
}

export const BoardGamePicker: FC<BoardGamePickerProps> = (props: BoardGamePickerProps) => {
  const { setSelectedCard, toggleCard, onList, cards } = props;
  const [ level, _setLevel ] = useState<CardLevel>(CardLevel.beginner);
  const [ type, _setType ] = useState<CardType|null>(null);
  const [ howToPlay, _setHowToPlay ] = useState<boolean>(false);
  const [ query, setQuery ] = useState<string>('');
  const { playToggle } = PlaySound();

  const setHowToPlay = (newVal: boolean) => {
    playToggle();
    return _setHowToPlay(newVal);
  };

  const setLevel = (newLevel: CardLevel) => {
    playToggle();
    return _setLevel(newLevel);
  };

  const setType = (newType: CardType|null) => {
    playToggle();
    return _setType(newType);
  };

  const customToggleCard = (card: Card) => {
    return () => {
      return toggleCard(card)();
    }
  };

  const toggleInfo = (card: Card) => {
    return () => {
      setSelectedCard(card);
    }
  };

  const cardsToDisplay = fuzzyfind(query, cards, {
    accessor: (card: Card) => {
      return `${card.name} ${card.displayName} ${card.definition}`;
    },
  }).filter((card: Card) => {
    if (type === null) return true;
    return type === card.type;
  }).filter((card: Card) => {
    if (level === CardLevel.all) return true;
    return card.level <= level;
  });

  return (
    <>
      <Row className="filters">
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant="success">
              {type === null ? (
                <span>Both Types</span>
              ) : (
                type === CardType.feeling ? (
                  <span>Feeling Cards</span>
                ) : (
                  <span>Need Cards</span>
                )
              )}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item
                active={type === null}
                onClick={() => setType(null)}>
                Both Types
              </Dropdown.Item>
              <Dropdown.Item active={type === CardType.feeling}
                onClick={() => setType(CardType.feeling)}>
                Feeling Cards
              </Dropdown.Item>
              <Dropdown.Item
                active={type === CardType.need}
                onClick={() => setType(CardType.need)}>
                Need Cards
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Col>
        <Col>
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
        </Col>
        <Col>
          <Form.Control
            size='lg'
            value={query}
            onChange={(ev) => setQuery(ev.target.value)}
            type="input"
            placeholder="Search..." />
        </Col>
        <Col className="info">
          <Button
            variant="info"
            onClick={() => setHowToPlay(!howToPlay) }>
            Help
          </Button>
        </Col>
      </Row>
      { howToPlay && (
        <Row>
          <p>
            If you're the <strong>speaker</strong> tell the listeners what's going
            on for you. Attempt to keep the bits small, and allow them to repeat
            them back to you. If you notice a feeling or need come up, add it to
            your list. The listeners can also suggest cards for you to add to your
            list. Once you're fully done talking, change the speaker and you'll
            become a listener.
          </p>
          <p>
            If you're the <strong>listener</strong> listen to what the user says,
            being as present as possible. Reflect back what the speaker says and
            make guesses at what they are feeling or needing. If you're having
            trouble, browse the card list. If the listener adds a feeling or need
            to their list, this will also be available to look at.
          </p>
        </Row>
      ) }
      <Row>
        { cardsToDisplay.length === 0 ? (
          <Alert variant="light">
            No cards were found. Try expanding your filters or removing your search term.
          </Alert>
        ) : (
          cardsToDisplay.map((card: Card) => {
            return (
              <Col key={card.id}>
                <GameCard
                  onList={onList(card)}
                  size={"lg"}
                  card={card}
                  handleInfo={toggleInfo(card)}
                  handleClick={customToggleCard(card)} />
              </Col>
            );
          })
        )}
      </Row>
    </>
  );
};
