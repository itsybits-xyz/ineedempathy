import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card, CardType } from '../schemas';
import { Button, Modal, ProgressBar, Card as CardEl, Row, Col, Container } from 'react-bootstrap';
import { MdInfoOutline } from 'react-icons/md';
import { Link } from 'react-router-dom';
import { CardPage } from './card-page';

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
  const [ infoCard, setInfoCard ] = useState<Card|undefined>();
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
            <div className='more-info'>
              <Link
                onClick={() => setInfoCard(card)}
                to={'#'}
                title={`Read more information on ${card.displayName}`}>
                <MdInfoOutline size={16} />
                <span>More Info</span>
              </Link>
            </div>
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
      { infoCard && (
        <Modal
          show={true}
          size='lg'
          onHide={() => setInfoCard(undefined) }>
          <Modal.Header closeButton>
            <Modal.Title>More information on {infoCard.displayName}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <CardPage match={{ params: infoCard }} />
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setInfoCard(undefined) }>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      )}
    </div>
  );
};
