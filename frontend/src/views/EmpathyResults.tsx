import React, { FC } from 'react';
import { BACKEND_URL } from '../config';
import { Card, CardType } from '../schemas';
import { ProgressBar, Card as CardEl, Row, Col, Container } from 'react-bootstrap';

export interface EmpathyResultsProps {
  cardGuesses: number[]
  cards: Card[]
}

export interface Result {
  count: number
  cardId: number
  card: Card|undefined
}

export const EmpathyResults: FC<EmpathyResultsProps> = (props: EmpathyResultsProps) => {
  const { cards, cardGuesses } = props;
  const totalGuesses = cardGuesses.length;

  const getCard = (id: number): Card|undefined => {
    return cards.find((card) => card.id === id);
  }

  const results = cardGuesses.reduce((memo: Result[], guess: number): Result[] => {
    const found = memo.find(({cardId}) => cardId === guess)
    if (!found) {
      memo.push({ count: 1, cardId: guess, card: getCard(guess)})
    } else {
      found.count++
    }
    return memo;
  }, []).sort((a, b) => {
    return b.count - a.count;
  });

  const feelingResults = results.filter(({card}) => {
    return card && card.type === CardType.feeling;
  });

  const needResults = results.filter(({card}) => {
    return card && card.type === CardType.need;
  });

  const displayCardWithResults = (count: number, card: Card) => {
    return (
      <Container fluid>
        <Row>
          <Col>
            <CardEl>
              <CardEl.Img
                alt={card.name}
                variant="top"
                src={ BACKEND_URL + card.image.md } />
              <CardEl.Body>
                <CardEl.Title>{card.displayName}</CardEl.Title>
              </CardEl.Body>
            </CardEl>
          </Col>
          <Col className="progress-col">
            <div>
              <ProgressBar
                striped
                srOnly
                label={`${count} Guesses`}
                variant="info"
                max={totalGuesses}
                now={count} />
            </div>
            <p>{count} Guesses</p>
          </Col>
        </Row>
      </Container>
    );
  }

  return (
    <div className="content fn-cards">
      <Container fluid>
        <Row>
          <Col>
            {feelingResults.map(({count, card}) => {
              return displayCardWithResults(count, card);
            })}
          </Col>
          <Col>
            {needResults.map(({count, card}) => {
              return displayCardWithResults(count, card);
            })}
          </Col>
        </Row>
      </Container>
    </div>
  );
};
