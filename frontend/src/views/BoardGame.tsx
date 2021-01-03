import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { createUser } from "../utils/api";
import { BACKEND_URL } from "../config";

export interface BoardGameProps {
  roomname: string;
  username: string;
}

interface Player {
  id: number;
  name: string;
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
  const [ status, setStatus ] = useState<number>(0);
  const [ waitingOn, setWaitingOn ] = useState<number[]>([]);
  const [ currentUsers, setCurrentUsers ] = useState<Player[]>([]);
  const pingEndpoint = () => { console.info('ping');sendMessage('{}'); };

  useEffect(() => {
    if (!lastMessage) return;
    const currentStatus: Message = JSON.parse(lastMessage.data);
    console.log('meow', currentStatus);
    if (!currentStatus) return;
    if (currentStatus.status) {
      setStatus(currentStatus.status);
    }
    if (currentStatus.waitingOn) {
      setWaitingOn(currentStatus.waitingOn);
    }
    if (currentStatus.currentUsers) {
      setCurrentUsers(currentStatus.currentUsers);
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
              <h2>User List</h2>
              <ul>
                { currentUsers.map((user: Player) => {
                  const isWaitingOn = waitingOn.includes(user.id);
                  return (
                    <li key={`user-${user.id}`}>
                      {user.name}
                      { isWaitingOn ? '*' : '' }
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
