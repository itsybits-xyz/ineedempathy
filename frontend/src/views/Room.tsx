import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from 'react-bootstrap';
import useWebSocket, { ReadyState } from "react-use-websocket";
import { createUser } from "../utils/api";
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

  if (!username) {
    /*
    createUser(roomname).then((user) => {
      localStorage.setItem(roomname, user.name);
      setUsername(user.name);
    });
     */
    return (
      <>
        <p>Creating your user...</p>
      </>
    );
  }

  return <BoardGame roomname={roomname} username={username} />

};
