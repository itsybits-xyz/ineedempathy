import { FC } from "react";
import { Badge, Button, Card as CardEl, Col, Row } from 'react-bootstrap';
import { Card } from "../schemas";
import { GameCard } from "../components";
import { Player } from '.';
import { MdChatBubble, MdHearing } from 'react-icons/md';

export interface CardListViewerProps {
  canChangeSpeaker: boolean;
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  changeSpeaker: (user: Player) => () => void;
  onList: (card: Card) => boolean;
  player?: Player;
  setSelectedCard: (card: Card|null) => void;
}

export const CardListViewer: FC<CardListViewerProps> = (props: CardListViewerProps) => {
  const {
    canChangeSpeaker,
    setSelectedCard,
    player,
    onList,
    toggleCard,
    changeSpeaker,
    cards
  } = props;
  return (
    <Row className={player?.speaker ? 'speaker' : 'listener'}>
      <CardEl className='users-cards'>
        <CardEl.Body>
          <CardEl.Title>
            { player && (
              <>
                <Row className={'player-info'}>
                  { player.speaker ? (
                    <Badge variant="success">
                      Speaker <MdChatBubble />
                    </Badge>
                  ) : (
                    <Badge variant="info">
                      Listener <MdHearing />
                    </Badge>
                  ) }&nbsp;
                  <span>
                    { player.name }
                  </span>
                </Row>
                {canChangeSpeaker && !player.speaker && (
                  <Row>
                    <Button
                      onClick={changeSpeaker(player)}
                      variant="outline-primary"
                      size="sm">Make Speaker</Button>
                  </Row>
                )}
              </>
            )}
          </CardEl.Title>
          <Row>
            { cards.length === 0 ? (
              <span>Try adding a card to your list.</span>
            ) : (
              cards.map((card: Card) => {
                return (
                  <Col key={card.id}>
                    <GameCard
                      onList={onList(card)}
                      size={'md'}
                      card={card}
                      handleInfo={() => setSelectedCard(card)}
                      handleClick={toggleCard(card)} />
                  </Col>
                );
              })
            )}
          </Row>
        </CardEl.Body>
      </CardEl>
    </Row>
  );
};
