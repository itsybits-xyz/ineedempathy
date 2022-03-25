import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card, CardType } from '../schemas';
import { Button, Row, Col, Container, Card as BootstrapCard } from 'react-bootstrap';
import { ClickSound } from '../components';

export interface SceneProps {
  setSelectedCard: (card: Card) => void,
  selectedCard ?: Card,
  cards: Card[],
  cardType: CardType,
  noun: string,
}

export const SceneCardPicker: FC<SceneProps> = (props: SceneProps) => {
  const [ seeMore, setSeeMore ] = useState<boolean>(false);
  const [ selectedCard, setSelectedCard ] = useState<Card|undefined>(props.selectedCard);
  const { cardType, cards, noun } = props;

  const isDefaultSelected = selectedCard && props.selectedCard && selectedCard.id === props.selectedCard.id;

  const toggleSelectedCard = (card: Card) => {
    if (!selectedCard || selectedCard.id !== card.id) {
      return setSelectedCard(card)
    }
    return setSelectedCard(undefined);
  }

  const handleSubmit = (card: Card) => {
    setSelectedCard(undefined);
    props.setSelectedCard(selectedCard)
  }

  const sortedCards = cards.filter((card: Card) => {
    return card.type === cardType;
  }).sort((a: Card, b: Card) => {
    const pos = a.level - b.level;
    if (pos !== 0) return pos;
    if (a.name < b.name) return -1;
    if (a.name > b.name) return 1;
    return 0;
  })

  const slicedCards = sortedCards.slice(0, seeMore ? sortedCards.length : 4);

  const showSubmitButton = selectedCard && !isDefaultSelected;

  return (
    <Container fluid>
      <Row>
        {slicedCards.map((card: Card) => {
          const isSelected = selectedCard && card.id === selectedCard.id;
          return (
            <Col key={card.id} onClick={() => toggleSelectedCard(card)}>
              <ClickSound>
                <BootstrapCard role="button" className={isSelected ? 'active' : 'inactive'}>
                  <BootstrapCard.Img
                    alt={card.name}
                    variant="top"
                    src={ BACKEND_URL + card.image.md } />
                  <BootstrapCard.Body>
                    <BootstrapCard.Title>{card.displayName}</BootstrapCard.Title>
                  </BootstrapCard.Body>
                </BootstrapCard>
              </ClickSound>
            </Col>
          );
        })}
      </Row>
      <Row>
      {!showSubmitButton && (
        <Button onClick={() => { setSeeMore(!seeMore) }} variant="success">
          See { seeMore ? 'Less' : 'All'} { cardType === CardType.feeling ? 'Feelings' : 'Needs' }
        </Button>
      )}
      {showSubmitButton && (
        <Button onClick={() => handleSubmit(selectedCard)} variant="success">
          Maybe {noun} was { cardType === CardType.feeling ? 'feeling' : 'needing' } <strong>{selectedCard.displayName}</strong>?
        </Button>
      )}
      </Row>
    </Container>
  );
};
