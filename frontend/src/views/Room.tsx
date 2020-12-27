import React, { FC } from 'react';
import { Container, Row } from 'react-bootstrap';

export interface RoomProps {
  match: {
    params: {
      name: string
    }
  }
}

export const Room: FC<RoomProps> = (props: RoomProps) => {
  const name = props?.match?.params?.name;
  return (
    <>
      <div className="content">
        <Container fluid>
          <Row>
            {name}
          </Row>
        </Container>
      </div>
    </>
  );
};
