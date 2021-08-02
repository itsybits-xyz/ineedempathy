import React, { FC, useState } from "react";
import {
  Card,
  InputGroup,
  FormControl,
  Button,
  Row
} from "react-bootstrap";
import { BoardGame } from "./BoardGame";
import { useAsync } from 'react-async';
import { getCards } from '../utils/api';
import { PlaySound } from "../components";

export interface RoomProps {
  match: {
    params: {
      name: string
    }
  }
}

export const Room: FC<RoomProps> = (props: RoomProps) => {
  const roomname = props?.match?.params?.name;
  const { data } = useAsync(getCards);
  const [username, setUsername] = useState<string>(localStorage.getItem(roomname) || "");
  const [ready, _setReady] = useState<boolean>(false);
  const { playToggle } = PlaySound();

  const setReady = (value:boolean) => {
    playToggle();
    localStorage.setItem(roomname, username);
    return _setReady(value);
  };

  if (!ready) {
    return (
      <Row>
        <Card style={{ marginLeft: '35px',  width: '35rem' }}>
          <Card.Body>
            <Card.Title>
              <p>Type in a <strong>display name</strong></p>
              <p>to join "{roomname}"!</p>
            </Card.Title>
            <Card.Title className="text-center">
              <InputGroup size="lg">
                <FormControl
                  placeholder="Type your display name here"
                  value={username}
                  onChange={(event) => {
                    setUsername(event.target.value);
                  }} />
              </InputGroup>
              <Button variant="success" onClick={() => setReady(true)}>
                Join Empathy Room
              </Button>
            </Card.Title>
          </Card.Body>
        </Card>
      </Row>
    );
  }

  return <BoardGame cards={data} roomname={roomname} username={username} />
};
