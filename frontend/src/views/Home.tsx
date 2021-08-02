import React, { FC } from "react";
import {
  Card,
  Button,
  Container,
  Row
} from "react-bootstrap";
import { PlaySound } from "../components";
import { JoinRoom } from ".";

export const Home: FC = () => {
  const { playToggle, playMatch, playNudge } = PlaySound();

  return (
    <Container className="content" style={{ width: '35rem' }} fluid>
      <JoinRoom />
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
