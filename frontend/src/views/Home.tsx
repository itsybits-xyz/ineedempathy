import React, { FC, useState, useEffect, useCallback } from "react";
import { Container, Row } from "react-bootstrap";
import {  postRoom } from "../utils/api";
import { RoomCreate } from "../schemas";
import { useForm } from "react-hook-form";
import { Redirect } from "react-router-dom";

export const Home: FC = () => {
  const { register, handleSubmit } = useForm();
  const [roomName, setRoomName] = useState<string>();

  const onSubmit = (roomData: RoomCreate) => {
    postRoom(roomData).then((newRoom) => {
      setRoomName(newRoom.name);
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
        </Container>
      </div>
    </>
  );
};
