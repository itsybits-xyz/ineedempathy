import React, { FC, useState, useEffect } from "react";
import { Alert, Button, Card as CardEl, Col, Container, Form, Modal, Row } from 'react-bootstrap'; import useWebSocket, { ReadyState } from "react-use-websocket"; import { Card } from "../schemas";
import { JoinRoom, BoardGamePicker, CardListViewer } from ".";
import './BoardGame.scss';
import { PlaySound } from "../components";
import { CardPage } from '.';
import { SOCKET_URL } from '../config';
import { Prompt } from "react-router-dom";

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
  const roomUrl = window.location.href;
  const { roomname, username, cards } = props;
  const socketUrl = `${SOCKET_URL}/rooms/${roomname}/users/${username}.ws`;
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [ currentUsers, setCurrentUsers ] = useState<Player[]>([]);
  const [ selectedCard, setSelectedCard ] = useState<Card|null>(null);
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
      if (currentUser?.speaker && currentUser !== user) {
        playToggle();
        sendMessage(JSON.stringify({changeSpeaker: user.name}))
      }
    };
  };

  useEffect(() => {
    window.onbeforeunload = function () {
      if (!!currentUser?.cards?.length || (currentUsers.length > 1)) {
        return "Are you sure you wish to leave the Empathy Room?";
      }
    };
  }, [currentUser, currentUsers])

  const copyRoom = () => {
    playToggle();
    const copyText = document.getElementById('roomUrl');
    copyText?.select();
    copyText?.setSelectionRange(0, 99999);
    document.execCommand("copy");
  };

  const isClosed = readyState === ReadyState.CLOSED;
  const isUninstantiated = readyState === ReadyState.UNINSTANTIATED;
  const isClosing = readyState === ReadyState.CLOSING;
  const isNotRecoverable = isClosing || isUninstantiated || isClosed;

  if (isNotRecoverable) {
    return (
      <>
        <Alert variant="warning">
          You have disconnected from your Empathy Room. Try checking your
          connection, and refreshing the page.
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
                setSelectedCard={setSelectedCard}
                toggleCard={toggleCard}
                onList={(card: Card) => {
                  return currentUser?.cards?.includes(card.id) || false;
                }} />
            </Row>
          </Col>
          <Col className="users-list">
            <Row>
              <CardEl>
                <CardEl.Body>
                  <CardEl.Title>Share Empathy Room</CardEl.Title>
                  <Form.Group className="mb-3">
                    <Form.Control readOnly type="text" id="roomUrl" value={roomUrl} />
                    <Form.Text className="text-muted">
                      Share this link to people you want to join the Empathy Room with you.
                    </Form.Text>
                  </Form.Group>
                  <Button variant="primary" onClick={copyRoom}>Copy URL</Button>
                </CardEl.Body>
              </CardEl>
            </Row>
            <Row>
              <h2>User List</h2>
            </Row>
            <Row>
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
                  <Row className="user-list" key={user.name}>
                    <CardListViewer
                      player={user}
                      setSelectedCard={setSelectedCard}
                      changeSpeaker={changeSpeaker}
                      toggleCard={toggleCard}
                      canChangeSpeaker={currentUser?.speaker || false}
                      onList={(card: Card):boolean => {
                        return currentUser?.cards?.includes(card.id) || false;
                      }}
                      cards={cards.filter((card) => {
                        return user.cards.includes(card.id)
                      })} />
                  </Row>
                );
              }) }
            </Row>
          </Col>
        </Row>
        { selectedCard && (
          <Modal
            show={true}
            size='lg'
            onHide={() => setSelectedCard(null) }>
            <Modal.Header closeButton>
              <Modal.Title>More information on {selectedCard.displayName}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <CardPage match={{ params: selectedCard }} />
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={() => setSelectedCard(null) }>
                Close
              </Button>
              { currentUser?.cards?.includes(selectedCard?.id) || false ? (
                <Button variant="primary" onClick={toggleCard(selectedCard)}>
                  Remove
                </Button>
              ) : (
                <Button variant="primary" onClick={toggleCard(selectedCard)}>
                  Add
                </Button>
              ) }
            </Modal.Footer>
          </Modal>
        ) }
        <Prompt when={!!currentUser?.cards?.length || (currentUsers.length > 1)} message="Are you sure you wish you leave the Empathy Room?"/>
      </Container>
    </>
  );
};
