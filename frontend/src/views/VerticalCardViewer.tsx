import { FC } from "react";
import { Col, Row } from 'react-bootstrap';
import { Card } from "../schemas";
import { GameCard } from "../components";
import './BoardGame.scss';
import { Player } from '.';

export interface VerticalCardViewerProps {
  cards: Card[];
  toggleCard: (card: Card) => () => void;
  onList: (card: Card) => boolean;
  player?: Player;
}

export const VerticalCardViewer: FC<VerticalCardViewerProps> = (props: VerticalCardViewerProps) => {
  const { player, onList, toggleCard, cards } = props;
  return (
    <Row className="vertical-card-list">
      { player?.name }
      { cards.map((card: Card) => {
        return (
          <Col>
            <GameCard
              onList={onList(card)}
              size={"lg"}
              card={card}
              handleClick={toggleCard(card)} />
          </Col>
        );
      })}
    </Row>
  );
};
