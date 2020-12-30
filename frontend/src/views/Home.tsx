import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from "react-bootstrap";
import { createUser, postRoom } from "../utils/api";
import { RoomCreate } from "../schemas";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";
import { BACKEND_URL } from "../config";
import useWebSocket, { ReadyState } from "react-use-websocket";

interface message {
  data: string;
}

export const Home: FC = () => {
  const socketUrl = `${BACKEND_URL.replace("http", "ws")}/ws`;
  const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);
  const { register, handleSubmit } = useForm();
  const [roomName, setRoomName] = useState<string>();
  const [messageHistory, setMessageHistory] = useState<message[]>([]);

  useEffect(() => {
    console.info('received', lastMessage);
    if (lastMessage) {
      setMessageHistory((prevHistory) => [...prevHistory, lastMessage]);
    }
  }, [lastMessage]);

  const handleClickSendMessage = useCallback(() => sendMessage(
    JSON.stringify({
      type: 'ROOM_JOIN',
      data: {
        room_id: 10,
        room_name: 'foo-bar',
        user_id: 11,
        user_name: 'princess.wiggles',
      }
    })
  ), []);

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  const onSubmit = (roomData: RoomCreate) => {
    postRoom(roomData).then((newRoom) => {
      return createUser(newRoom.name).then((user) => {
        setRoomName(newRoom.name);
      });
    });
  };

  return roomName ? (
    <Redirect to={`/room/${roomName}`} />
  ) : (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <form onSubmit={handleSubmit(onSubmit)}>
              <label>
                Room Type
                <select name="type" ref={register}>
                  <option value="singleplayer">Singleplayer</option>
                  <option value="multiplayer">Multiplayer</option>
                  <option value="public-multiplayer">Public Multiplayer</option>
                </select>
              </label>
              <input type="submit" value="Create Room" />
            </form>
          </Row>
          <Row>
            <div>
              <button
                onClick={handleClickSendMessage}
                disabled={readyState !== ReadyState.OPEN}
              >
                Click Me to send 'Hello'
              </button>
              <p>Socket URL: {socketUrl}</p>
              <p>The WebSocket is currently {connectionStatus}</p>
              {(lastMessage && <p>Last message: {lastMessage.data}</p>) || (
                <p>No last message</p>
              )}
              <ul>
                {messageHistory.map((message, idx) => (
                  <li key={idx}>{message.data}</li>
                ))}
              </ul>
            </div>
          </Row>
        </Container>
      </div>
    </>
  );
};
