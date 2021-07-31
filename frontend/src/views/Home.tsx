import React, { FC, useState, useEffect, useCallback } from "react";
import { Button, Container, Row } from "react-bootstrap";
import { createRoom } from "../utils/api";
import { RoomCreate } from "../schemas";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";
import { Hidden } from "../components";
import useSound from 'use-sound';

import nudgePersonSound from '../sound/rising-pops.mp3';
import toggleCardSound from '../sound/pop-up-off.mp3';
import matchSound from '../sound/fanfare.mp3';

export const Home: FC = () => {
  const [gotoRoomName, setGotoRoomName] = useState<string>();
  const [roomName, setRoomName] = useState<string>();
  const [error, setError] = useState<string>();
  const [playMatchSound] = useSound(matchSound);
  const [playToggleCardSound] = useSound(toggleCardSound);
  const [playNudgePersonSound] = useSound(nudgePersonSound);

  const handleNewRoom = (ev:any) => {
    ev.preventDefault();
    return createRoom().then((newRoom) => {
      setGotoRoomName(newRoom.name);
    }).catch((er) => {
      setError(er);
    });
  };

  const handleJoinRoom = () => {
    setGotoRoomName(roomName);
  };

  if (error) {
    return (
      <Hidden error={error} />
    );
  }

  return gotoRoomName ? (
    <Redirect to={`/room/${gotoRoomName}`} />
  ) : (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <form onSubmit={handleNewRoom}>
              <input type="submit" value="Create Room" />
            </form>
          </Row>
          <Row>
            <form onSubmit={handleJoinRoom}>
              <input type="text" value={roomName} onChange={(event) => {
                setRoomName(event.target.value);
              }} />
              <input type="submit" value="Join Room" />
            </form>
          </Row>
        </Container>
        <Container>
          <Row>
            <Button onClick={() => playMatchSound() }>Match Sound</Button>
            <Button onClick={() => playToggleCardSound() }>Toggle Card</Button>
            <Button onClick={() => playNudgePersonSound() }>Nudge Person</Button>
          </Row>
        </Container>
      </div>
    </>
  );
};
