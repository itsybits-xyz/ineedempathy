import React, { FC, useState, useEffect } from "react";
import { Alert, Col, Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BACKEND_URL } from "../config";
import { Card } from "../schemas";
import { JoinRoom, BoardGamePicker, CardListViewer } from ".";
import './BoardGame.scss';
import { PlaySound } from "../components";

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
  const socketUrl = `${window.location.origin.replace("http", "ws")}/api/rooms/${roomname}/users/${username}.ws`;
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [ currentUsers, setCurrentUsers ] = useState<Player[]>([]);
  const { playToggle } = PlaySound();

  useEffect(() => {
    if (!lastMessage) return;
    const currentStatus: Message = JSON.parse(lastMessage.data);
    if (!currentStatus) return;
    if (currentStatus.users) {
      setCurrentUsers(currentStatus.users);
    }
  }, [lastMessage]);

  const toggleCard = (card: Card) => {
    return () => {
      playToggle();
      sendMessage(JSON.stringify({toggleCard: card.id}))
    };
  };


  const currentUser = currentUsers.find((user: Player) => {
    return user.name === username;
  });

  const changeSpeaker = (user: Player) => {
    return () => {
      if (currentUser.speaker && currentUser !== user) {
        playToggle();
        sendMessage(JSON.stringify({changeSpeaker: user.name}))
      }
    };
  };

  const isClosed = readyState === ReadyState.CLOSED;
  const isUninstantiated = readyState === ReadyState.UNINSTANTIATED;
  const isClosing = readyState === ReadyState.CLOSING;
  const isNotRecoverable = isClosing || isUninstantiated || isClosed;

  if (isNotRecoverable) {
    return (
      <>
        <Alert variant="warning">
          This room "{roomname}" does not exist.
        </Alert>
        <JoinRoom oldRoomName={roomname} />
      </>
    );
  }

  return (
    <>
      <Container className="content board-game" fluid>
        <Row className="cards-users">
          <Col className="cards-list">
            <Row className="big-card-list">
              <BoardGamePicker
                cards={cards}
                toggleCard={toggleCard}
                onList={(card: Card) => {
                  return currentUser?.cards?.includes(card.id) || false;
                }} />
            </Row>
          </Col>
          <Col className="users-list">
            <h2>User List</h2>
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
                  key={user.name}
                  player={user}
                  changeSpeaker={changeSpeaker}
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
