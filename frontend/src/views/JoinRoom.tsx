import { FC, useState } from "react";
import {
  Card,
  Button,
  Row } from "react-bootstrap";
import { generateName } from "../utils";
import { Redirect } from "react-router-dom";
import { PlaySound } from "../components";

export const JoinRoom: FC = () => {
  const [gotoRoomName, setGotoRoomName] = useState<string>();
  const { playToggle } = PlaySound();

  const handleNewRoom = () => {
    playToggle();
    setGotoRoomName(generateName());
  };

  return gotoRoomName ? (
    <Redirect to={`/room/${gotoRoomName}`} />
  ) : (
    <>
      <Row className="justify-content-md-center">
        <Card className="responsive">
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
    </>
  );
};
