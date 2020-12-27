import React, { FC, useState } from 'react';
import { Container, Row } from 'react-bootstrap';
import { postRoom } from '../utils/api';
import { RoomCreate } from '../schemas';
import { useForm } from "react-hook-form";

export const Home: FC = () => {
  const { register, handleSubmit } = useForm();
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const onSubmit = (data: RoomCreate) => {
    setIsLoading(true);
    postRoom(data).then((data) => {
      debugger;
    });
  };

  return isLoading ? (
    <>
      <label>Loading...</label>
    </>
  ) : (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <form onSubmit={handleSubmit(onSubmit)}>
              <label>Room Type
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
