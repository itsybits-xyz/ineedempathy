import { FC, useState } from "react";
import {
  Card,
  InputGroup,
  FormControl,
  Button,
  Container,
  Row
} from "react-bootstrap";
import { createRoom } from "../utils/api";
import { Redirect } from "react-router-dom";
import { PlaySound, Hidden } from "../components";

export interface JoinRoomProps {
  oldRoomName?: string;
}

export const JoinRoom: FC<JoinRoomProps> = (props: JoinRoomProps) => {
  const { oldRoomName } = props;
  const [gotoRoomName, setGotoRoomName] = useState<string>();
  const [roomName, setRoomName] = useState<string>(oldRoomName || '');
  const [error, setError] = useState<string>();
  const { playToggle } = PlaySound();

  const handleNewRoom = () => {
    playToggle();
    return createRoom().then((newRoom) => {
      setGotoRoomName(newRoom.name);
    }).catch((er) => {
      setError(er);
    });
  };

  const handleJoinRoom = () => {
    playToggle();
    if (roomName !== oldRoomName && String(roomName).length > 0) {
      setGotoRoomName(roomName);
    }
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
              <Button onClick={handleNewRoom} variant="success" size="lg">
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
            <Card.Title>
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
            </Card.Title>
          </Card.Body>
        </Card>
      </Row>
    </Container>
  );
};
