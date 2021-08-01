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

  const currentUser = currentUsers.filter((user: Player) => {
    return user.name === username;
  });
  
  const speaker = currentUsers.filter((user: Player) => {
    return user.speaker;
  });

  return (
    <>
      <div className="content board-game">
        <Container fluid>
          <Row>
            <Col>
              <Row className="big-card-list">
                { cards.map((card) => {
                  const onList = currentUser?.cards?.includes(card.id)
                  console.log(currentUser);
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
            <Col>
              <h2>User List {connectionStatus}</h2>
              { currentUsers.filter((user: Player) => {
                return !user.speaker;
              }).map((user: Player) => {
                return (
                  <div key={`user-${user.name}`}>
                    {user.name}
                    <Row>
                      {cards
                        .filter((card) => user.cards.includes(card.id))
                        .map((card) => {
                          const onList = currentUser?.cards?.includes(card.id)
                          return (
                            <Col>
                              <GameCard
                                onList={onList}
                                size={"md"}
                                card={card}
                                handleClick={toggleCard(card)} />
                            </Col>
                          )}
                        )
                      }
                    </Row>
                  </div>
                );
              }) }
            </Col>
          </Row>
          <Row>
            <Col>
              { speaker.map((user: Player) => {
                return (
                    <Row>
                      {cards
                        .filter((card) => user.cards.includes(card.id))
                        .map((card) => {
                          const onList = currentUser?.cards?.includes(card.id)
                          return (
                            <Col>
                              <GameCard
                                onList={onList}
                                size={"lg"}
                                card={card}
                                handleClick={toggleCard(card)} />
                            </Col>
                          )}
                        )
                      }
                    </Row>
                );
              }) }
            </Col>
          </Row>
        </Container>
      </div>
    </>
  );
};
