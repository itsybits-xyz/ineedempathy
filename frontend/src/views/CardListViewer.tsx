import { FC } from "react";
import { Col, Row } from 'react-bootstrap';
import { Card } from "../schemas";
import { GameCard } from "../components";
import './BoardGame.scss';
import { Player } from '.';
import { MdChatBubble, MdHearing } from 'react-icons/md';

export interface CardListViewerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  onList: (card: Card) => boolean;
  player?: Player;
}

export const CardListViewer: FC<CardListViewerProps> = (props: CardListViewerProps) => {
  const { player, onList, toggleCard, cards } = props;
  return (
    <Row className={player?.speaker ? 'speaker' : 'listener'}>
      { player && (
        <Row className={'player-info'}>
          { player.speaker ? (
            <span>
              Speaker <MdChatBubble />
            </span>
          ) : (
            <span>
              Listener <MdHearing />
            </span>
          ) }
          { player.name }
        </Row>
      ) }
      <Row className={'cards'}>
        { cards.map((card: Card) => {
          return (
            <Col>
              <GameCard
                onList={onList(card)}
                size={'md'}
                card={card}
                handleClick={toggleCard(card)} />
            </Col>
          );
        })}
      </Row>
    </Row>
  );
};
