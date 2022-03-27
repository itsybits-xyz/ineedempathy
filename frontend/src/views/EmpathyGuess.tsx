import React, { FC, useEffect, useState } from 'react';
import { Card, CardType } from '../schemas';
import { Container, Row, Button } from 'react-bootstrap';
import { SceneCardPicker } from './SceneCardPicker';

export interface EmpathyGuessProps {
  cards: Card[]
  noun: string
  rerender: number
  onSubmit: (cards: Card[]) => void
}

export const EmpathyGuess: FC<EmpathyGuessProps> = (props: EmpathyGuessProps) => {
  const { rerender, cards, noun } = props;
  const [ cachedRenderId, setCachedRenderId ] = useState<number>();
  const [ feelingCard, setFeelingCard ] = useState<Card>();
  const [ needCard, setNeedCard ] = useState<Card>();
  const [ cardType, setCardType ] = useState<CardType>(CardType.feeling);


  useEffect(() => {
    if (rerender !== cachedRenderId) {
      console.log('Parent asked for a reset', rerender);
      setCachedRenderId(rerender);
      if (feelingCard) {
        setFeelingCard(undefined);
      }
      if (needCard) {
        setNeedCard(undefined);
      }
      if (cardType !== CardType.feeling) {
        setCardType(CardType.feeling);
      }
    }
  }, [rerender, cachedRenderId, feelingCard, needCard, cardType]);


  const handleNext = (card: Card) => {
    if (!feelingCard) {
      setFeelingCard(card);
      setCardType(CardType.need)
    } else {
      setNeedCard(card)
    }
  };

  const handleSubmit = () => {
    return props.onSubmit([
      feelingCard,
      needCard,
    ])
  }

  return feelingCard && needCard ? (
    <Container className="guess" fluid>
      <Row>
        <h3>Empathy Guess</h3>
      </Row>
      <Row>
        <p>Is {noun} feeling <strong>{feelingCard.displayName}</strong> and needing <strong>{needCard.displayName}</strong>?</p>
      </Row>
      <Row>
        <Button size="lg" variant="primary" onClick={handleSubmit}>Ask {noun}</Button>
      </Row>
    </Container>
  ) : (
    <Container fluid>
      <div className="content fn-cards">
        <h3>What do you think { noun } was <strong>{ cardType === CardType.feeling ? 'feeling' : 'needing' }</strong>?</h3>
        <SceneCardPicker
          noun={noun}
          cardType={cardType}
          setSelectedCard={(card: Card) => handleNext(card)}
          selectedCard={cardType === CardType.feeling ? feelingCard : needCard}
          cards={cards} />
      </div>
    </Container>
  );
};
