import React, { FC, useState } from "react";
import { ButtonGroup, Button, Dropdown, Col, Row } from 'react-bootstrap';
import { PlaySound, GameCard } from "../components";
import { CardLevel, CardType, Card } from "../schemas";

export interface BoardGamePickerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  onList: (card: Card) => boolean;
}

export const BoardGamePicker: FC<BoardGamePickerProps> = (props: BoardGamePickerProps) => {
  const { toggleCard, onList, cards } = props;
  const [ level, _setLevel ] = useState<CardLevel>(CardLevel.beginner);
  const [ type, _setType ] = useState<CardType|null>(null);
  const [ howToPlay, _setHowToPlay ] = useState<boolean>(false);
  const { playToggle } = PlaySound();

  const isCardLevel = (lookLevel: CardLevel, success: any, fail: any):any => {
    return lookLevel === level ? success : fail;
  };

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

  return (
    <>
      <Row className="filters">
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant="success">
              {type === null ? (
                <span>Both Cards</span>
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
                Both Cards
              </Dropdown.Item>
              <Dropdown.Item
                active={type === CardType.feeling}
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
        { cards
          .filter((card: Card) => {
            if (type === null) return true;
            return type === card.type;
          }).filter((card: Card) => {
            if (level === CardLevel.all) return true;
            return card.level <= level;
          }).map((card: Card, idx: number) => {
            return (
              <Col key={idx}>
                <GameCard
                  onList={onList(card)}
                  size={"lg"}
                  card={card}
                  handleClick={toggleCard(card)} />
              </Col>
            );
          }
        )}
      </Row>
    </>
  );
};
