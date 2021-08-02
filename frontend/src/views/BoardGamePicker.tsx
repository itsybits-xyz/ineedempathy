import React, { FC, useState } from "react";
import { ButtonGroup, Button, Dropdown, Col, Row } from 'react-bootstrap';
import { GameCard } from "../components";
import { CardLevel, CardType, Card } from "../schemas";

export interface BoardGamePickerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  onList: (card: Card) => boolean;
}

export const BoardGamePicker: FC<BoardGamePickerProps> = (props: BoardGamePickerProps) => {
  const { toggleCard, onList, cards } = props;
  const [ level, setLevel ] = useState<CardLevel>(CardLevel.beginner);
  const [ type, setType ] = useState<CardType|null>(null);

  const isCardLevel = (lookLevel: CardLevel, success: any, fail: any):any => {
    return lookLevel === level ? success : fail;
  }

  return (
    <>
      <Row className="filters">
        <Col>
          <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
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
                Both
              </Dropdown.Item>
              <Dropdown.Item
                active={type === CardType.feeling}
                onClick={() => setType(CardType.feeling)}>
                Feelings
              </Dropdown.Item>
              <Dropdown.Item
                active={type === CardType.need}
                onClick={() => setType(CardType.need)}>
                Needs
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
      </Row>
      <Row>
        { cards
          .filter((card: Card) => {
            if (type === null) return true;
            return type === card.type;
          }).filter((card: Card) => {
            if (level === CardLevel.all) return true;
            return card.level <= level;
          }).map((card: Card) => {
            return (
              <Col>
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
