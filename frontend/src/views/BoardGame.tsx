import React, { FC, useState, useEffect } from "react";
import { Col, Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BACKEND_URL } from "../config";
import { GameCard } from "../components";
import { Card } from "../schemas";
import { CardListViewer } from ".";
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
            { currentUsers.sort((user1: Player, user2: Player) => {
              // Speaker first
              if (user1.speaker) return -1;
              if (user2.speaker) return 1;
              // Name second
              if (user1.name > user2.name) return -1;
              if (user2.name > user1.name) return 1;
              return 0;
            }).map((user: Player) => {
              return (
                <CardListViewer
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
      </Container>
    </>
  );
};
