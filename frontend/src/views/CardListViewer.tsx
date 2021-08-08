import { FC } from "react";
import { Card as CardEl, Col, Row } from 'react-bootstrap';
import { Card } from "../schemas";
import { GameCard } from "../components";
import { Player } from '.';
import { MdChatBubble, MdHearing } from 'react-icons/md';

export interface CardListViewerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  changeSpeaker: (user: Player) => () => void;
  onList: (card: Card) => boolean;
  player?: Player;
  setSelectedCard: (card: Card|null) => void;
}

export const CardListViewer: FC<CardListViewerProps> = (props: CardListViewerProps) => {
  const { setSelectedCard, player, onList, toggleCard, changeSpeaker, cards } = props;
  return (
    <Row className={player?.speaker ? 'speaker' : 'listener'}>
      <CardEl className='users-cards'>
        <CardEl.Body>
          <CardEl.Title>
            { player && (
              <Row 
                className={'player-info'}>
                { player.speaker ? (
                  <span>
                    Speaker <MdChatBubble />
                  </span>
                ) : (
                  <span>
                    Listener <MdHearing />
                  </span>
                ) }
                <span onClick={changeSpeaker(player)}>
                  { player.name }
                </span>
              </Row>
            ) }
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
