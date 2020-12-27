import React, { FC, useState } from 'react';
import { Container, Col, Row } from 'react-bootstrap';
import { postRoom } from '../utils/api';
import { useAsync } from 'react-async';
import { BACKEND_URL } from '../config';
import { RoomType, RoomCreate } from '../schemas';
import { useForm } from "react-hook-form";

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
