import React, { FC, useState } from "react";
import { Card, InputGroup, FormControl, Button, Container, Col, Row } from "react-bootstrap";
import { createRoom } from "../utils/api";
import { Redirect } from "react-router-dom";
import { PlaySound, Hidden } from "../components";

export const Home: FC = () => {
  const [gotoRoomName, setGotoRoomName] = useState<string>();
  const [roomName, setRoomName] = useState<string>();
  const [error, setError] = useState<string>();
  const { playToggle, playMatch, playNudge } = PlaySound();

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

  const styles = {
    width: '35rem',
  };

  if (error) {
    return (
      <Hidden error={error} />
    );
  }

  return gotoRoomName ? (
    <Redirect to={`/room/${gotoRoomName}`} />
  ) : (
    <Container className="content" style={styles} fluid>
      <Row className="justify-content-md-center">
        <Card style={{ width: '35rem' }}>
          <Card.Body>
            <Card.Title>
              Would you like to meet your need for <strong>empathy</strong>?
            </Card.Title>
            <Card.Text className="text-center">
              <Button onSubmit={handleNewRoom} variant="success" size="lg">
                Create an Empathy Room
              </Button>
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>
      <Row className="justify-content-md-center">
        <Card style={{ width: '35rem' }}>
          <Card.Body>
            <Card.Title>
              Join an existing Empathy Room
            </Card.Title>
            <Card.Text className="text-center">
              <InputGroup size="lg">
                <FormControl
                  placeholder="Type the Empathy Room key here"
                  value={roomName}
                  onChange={(event) => {
                    setRoomName(event.target.value);
                  }} />
              </InputGroup>
              <Button variant="success" onClick={handleJoinRoom}>
                Join Empathy Room
              </Button>
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>
      <Row className="justify-content-md-center">
        <Card style={{ width: '35rem' }}>
          <Card.Body>
            <Card.Title>
              Play with our cute sounds :)
            </Card.Title>
            <Card.Text className="text-center">
              <Button onClick={() => playMatch() }>Match Sound</Button>
              <Button onClick={() => playToggle() }>Toggle Card</Button>
              <Button onClick={() => playNudge() }>Nudge Person</Button>
            </Card.Text>
          </Card.Body>
        </Card>
      </Row>
    </Container>
  );
};
