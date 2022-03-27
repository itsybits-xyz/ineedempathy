import React, { FC, useState } from 'react';
import { BACKEND_URL } from '../config';
import { Card, CardType } from '../schemas';
import { Modal, Button, Row, Col, Container, Card as BootstrapCard } from 'react-bootstrap';
import { CardPage } from './card-page';
import { ClickSound } from '../components';
import { MdInfoOutline } from 'react-icons/md';
import { Link } from 'react-router-dom';

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
  const [ infoCard, setInfoCard ] = useState<Card|undefined>();

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
    <>
      <Container fluid>
        <Row>
          {slicedCards.map((card: Card) => {
            const isSelected = selectedCard && card.id === selectedCard.id;
            return (
              <Col className="scene-card" key={card.id}>
                <ClickSound>
                  <BootstrapCard
                    onClick={() => toggleSelectedCard(card)}
                    className={isSelected ? 'active' : 'inactive'}>
                    <BootstrapCard.Img
                      alt={card.name}
                      variant="top"
                      src={ BACKEND_URL + card.image.md } />
                    <BootstrapCard.Body>
                      <BootstrapCard.Title>{card.displayName}</BootstrapCard.Title>
                    </BootstrapCard.Body>
                  </BootstrapCard>
                  <div className='more-info'>
                    <Link
                      onClick={() => setInfoCard(card)}
                      to={'#'}
                      title={`Read more information on ${card.displayName}`}>
                      <MdInfoOutline size={16} />
                      <span>More Info</span>
                    </Link>
                  </div>
                </ClickSound>
              </Col>
            );
          })}
        </Row>
        <Row>
        {!showSubmitButton && (
          <Button size="lg" onClick={() => { setSeeMore(!seeMore) }} variant="success">
            See { seeMore ? 'Less' : 'All'} { cardType === CardType.feeling ? 'Feelings' : 'Needs' }
          </Button>
        )}
        {showSubmitButton && (
          <Button size="lg" onClick={() => handleSubmit(selectedCard)} variant="success">
            Maybe {noun} was { cardType === CardType.feeling ? 'feeling' : 'needing' } <strong>{selectedCard.displayName}</strong>?
          </Button>
        )}
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
    </>
  );
};
