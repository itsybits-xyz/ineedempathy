import React, { FC, useState, useEffect, useCallback } from "react";
import { Button, Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { BoardGame } from "./BoardGame";
import { BACKEND_URL } from "../config";

export interface RoomProps {
  match: {
    params: {
      name: string
    }
  }
}

export const Room: FC<RoomProps> = (props: RoomProps) => {
  const roomname = props?.match?.params?.name;
  const [username, setUsername] = useState<string>(localStorage.getItem(roomname) || "");
  const [ready, _setReady] = useState<boolean>(false);

  const setReady = (value) => {
    localStorage.setItem(roomname, username);
    return _setReady(value);
  };

  if (!ready) {
    return (
      <>
        <div>
          Type in your username to join {roomname}
        </div>
        <div>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value) } />
        </div>
        <div>
          <Button onClick={() => setReady(true)}>Join Now</Button>
        </div>
      </>
    );
  }

  return <BoardGame roomname={roomname} username={username} />
};
