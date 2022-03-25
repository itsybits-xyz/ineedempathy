import React, { FC } from "react";
import {
  Card,
  Container,
  Row
} from "react-bootstrap";
import { JoinRoom } from ".";

export const Home: FC = () => {
  return (
    <Container className="content" fluid>
      <Row className="justify-content-md-center">
        <Card className="logo responsive">
          <Card.Body>
            <img
              alt="I Need Empathy Logo - Blue background, with a rainbow coming from a cloud"
              src="/logo.png"
            />
          </Card.Body>
        </Card>
      </Row>
      <JoinRoom />
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
              Create an Empathy Room, invite people to join, and they can make
              an empathy guess about what you are feeling and needing. Work
              together to collaborate on understanding an experience you are
              going through, that you'd like to <strong>be heard</strong>{' '}
              on or a conflict between you and others.
            </p>
            <p>
              <strong>Connect</strong> and <strong>empathize</strong> with{' '}
              yourself and others today.
            </p>
          </Card.Body>
        </Card>
      </Row>
    </Container>
  );
};
