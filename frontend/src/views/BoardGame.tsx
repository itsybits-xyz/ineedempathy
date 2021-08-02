import React, { FC, useState, useEffect } from "react";
import { Col, Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BACKEND_URL } from "../config";
import { GameCard } from "../components";
import { Card } from "../schemas";
import { VerticalCardViewer } from ".";
import './BoardGame.scss';

export interface BoardGameProps {
  cards: Card[];
  roomname: string;
  username: string;
}

export interface Player {
  name: string;
  speaker: boolean;
  cards: number[];
}

interface Message {
  users: Player[],
}

export const BoardGame: FC<BoardGameProps> = (props: BoardGameProps) => {
  const { roomname, username, cards } = props;
  const socketUrl = `${BACKEND_URL.replace("http", "ws")}/rooms/${roomname}/users/${username}.ws`;
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [ currentUsers, setCurrentUsers ] = useState<Player[]>([]);

  useEffect(() => {
    if (!lastMessage) return;
    const currentStatus: Message = JSON.parse(lastMessage.data);
    if (!currentStatus) return;
    if (currentStatus.users) {
      setCurrentUsers(currentStatus.users);
    }
  }, [lastMessage]);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  const toggleCard = (card: Card) => {
    return () => {
      sendMessage(String(card.id))
    }
  };

  const currentUser = currentUsers.find((user: Player) => {
    return user.name === username;
  });
  
  const speaker = currentUsers.find((user: Player) => {
    return user.speaker;
  });

  return (
    <>
      <Container className="content board-game" fluid>
        <Row className="cards-users">
          <Col className="cards-list">
            <Row className="big-card-list">
              { cards.map((card) => {
                const onList = currentUser?.cards?.includes(card.id) || false;
                return (
                  <Col>
                    <GameCard
                      onList={onList}
                      size={"lg"}
                      card={card}
                      handleClick={toggleCard(card)} />
                  </Col>
                );
              })}
            </Row>
          </Col>
          <Col className="users-list">
            <h2>User List {connectionStatus}</h2>
            { currentUsers.filter((user: Player) => {
              return !user.speaker;
            }).map((user: Player) => {
              return (
                <VerticalCardViewer
                  key={`user-${user.name}`}
                  player={user}
                  toggleCard={toggleCard}
                  onList={(card: Card):boolean => {
                    return currentUser?.cards?.includes(card.id) || false;
                  }}
                  cards={cards.filter((card) => {
                    return user.cards.includes(card.id)
                  })} />
              );
            }) }
          </Col>
        </Row>
        <Row className="speaker">
          <Col className="speaker-list">
            <VerticalCardViewer
              player={speaker}
              toggleCard={toggleCard}
              onList={(card: Card) => {
                return true;
              }}
              cards={cards.filter((card) => {
                return speaker?.cards.includes(card.id)
              })} />
          </Col>
        </Row>
      </Container>
    </>
  );
};
