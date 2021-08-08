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
    <Container className="content" fluid>
      <Row className="justify-content-md-center">
        <Card className="responsive">
          <Card.Body>
            <Card.Title>
              I Need Empathy
            </Card.Title>
            <p>
              Discover what you are feeling and needing, by giving yourself{' '}
              <strong>empathy</strong>. Browse through the Feeling and Need
              pages and learn more about each card and how it might relate to
              your personal experiences.
            </p>
            <p>
              Work together to collaborate on understanding an experience you
              are going through, that you'd like to <strong>be heard</strong>{' '}
              on or a conflict between you and others. Create an Empathy Room,
              invite people to join, and they can make an empathy guess about
              what you are feeling and needing.
            </p>
            <p>
              <strong>Connect</strong> and <strong>empathize</strong> with{' '}
              yourself and others today.
            </p>
          </Card.Body>
        </Card>
      </Row>
      <JoinRoom />
      <Row className="justify-content-md-center">
        <Card className="responsive">
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
