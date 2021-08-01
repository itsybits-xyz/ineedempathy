import React, { FC, useState, useEffect } from "react";
import { Col, Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BACKEND_URL } from "../config";
import { GameCard } from "../components";
import { Card } from "../schemas";

export interface BoardGameProps {
  cards: Card[];
  roomname: string;
  username: string;
}

interface Player {
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

  return (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <div>
              <h2>User List {connectionStatus}</h2>
              <ul>
                { currentUsers.map((user: Player) => {
                  return (
                    <li key={`user-${user.name}`}>
                      {user.name}
                      {cards
                          .filter((card) => user.cards.includes(card.id))
                          .map((card) => { 
                            return (
                              <Col>
                                <GameCard card={card}/>
                              </Col>
                            )}
                          )
                      }
                    </li>
                  );
                }) }
              </ul>
            </div>
          </Row>
          <Row>
            { cards.map((card) => {
              return (
                <Col>
                  <GameCard
                    card={card}
                    handleClick={toggleCard(card)} />
                </Col>
              );
            })}
          </Row>
        </Container>
      </div>
    </>
  );
};
