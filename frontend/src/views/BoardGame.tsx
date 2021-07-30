import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BACKEND_URL } from "../config";

export interface BoardGameProps {
  roomname: string;
  username: string;
}

interface Player {
  name: string;
  speaker: boolean;
  cards: number[];
}

interface Message {
  status: number,
  waitingOn: number[],
  currentUsers: Player[],
}

export const BoardGame: FC<BoardGameProps> = (props: BoardGameProps) => {
  const { roomname, username } = props;
  const socketUrl = `${BACKEND_URL.replace("http", "ws")}/rooms/${roomname}/users/${username}.ws`;
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const [ currentUsers, setCurrentUsers ] = useState<Player[]>([]);
  const pingEndpoint = () => { console.info('ping');sendMessage('{}'); };

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

  return (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <div>
              <h2>User List {username}</h2>
              <ul>
                { currentUsers.map((user: Player) => {
                  return (
                    <li key={`user-${user.name}`}>
                      {user.name}
                    </li>
                  );
                }) }
              </ul>
            </div>
          </Row>
        </Container>
      </div>
    </>
  );
};
