import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from "react-bootstrap";
import { createRoom } from "../utils/api";
import { RoomCreate } from "../schemas";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";
import { Hidden } from "../components";

export const Home: FC = () => {
  const [gotoRoomName, setGotoRoomName] = useState<string>();
  const [roomName, setRoomName] = useState<string>();
  const [error, setError] = useState<string>();

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
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={error} />
      </>
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
      </div>
    </>
  );
};
