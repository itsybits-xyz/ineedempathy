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

  const handleNewRoom = (ev:any, count = 0) => {
    fetch("http://localhost:8000/rooms", {
      "body": "{}",
      "method": "POST",
    }).then((res) => {
      console.log('BS:2', res);
    }, (er) => {
      console.log('BS:2', er, er.message, er.stack);
    });
    return;
    console.log('BS: Attempting room creation', count);
    return createRoom().then((newRoom) => {
      console.log('BS: Setting room:', newRoom.name);
      setGotoRoomName(newRoom.name);
    }).catch((er) => {
      if (count < 10) {
        console.log('BS: loop');
        handleNewRoom(ev, count + 1);
      } else {
        console.log('BS: fucckckk', er, er.message, er.stack);
      }
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

  return gotoRoomName && false ? (
    <div>to={`/room/${gotoRoomName}`};</div>
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
