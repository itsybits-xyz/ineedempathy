import React, { FC, useState } from 'react';
import { Container, Col, Row } from 'react-bootstrap';

export const Home: FC = () => {
  const [clicks, setClicks] = useState<number>(0);

  return (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            <p>You clicked me {clicks} times. Are you not entertained?</p>
            <button onClick={() => setClicks(clicks +1)}>
              Click me
            </button>
          </Row>
        </Container>
      </div>
    </>
  );
};
