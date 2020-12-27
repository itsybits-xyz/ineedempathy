import React, { FC, useState } from 'react';
import { Container, Col, Row } from 'react-bootstrap';
import { getCards } from '../utils/api';
import { useAsync } from 'react-async';
import { BACKEND_URL } from '../config';

export const Home: FC = () => {
  const { data, error, isPending } = useAsync(getCards);
  const [offset, setOffset] = useState<number>(0);

  const nextPage = () => setOffset(offset + 1);
  const prevPage = () => setOffset(offset === 0 ? offset : offset - 1);

  return isPending || error || !data ? (
    <>
      <div className="content">
        Loading...
      </div>
    </>
  ) : (
    <div className="content">
      <Container fluid>
        <Row>
          <Col xs={1} onClick={prevPage}>Prev</Col>
          <Col>
            <Row>
              <Col>
                <img width={200} src={BACKEND_URL + data[0 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[1 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[2 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[3 + offset].textUrl} />
              </Col>
            </Row>
            <Row>
              <Col>
                <img width={200} src={BACKEND_URL + data[4 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[5 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[6 + offset].textUrl} />
              </Col>
              <Col>
                <img width={200} src={BACKEND_URL + data[7 + offset].textUrl} />
              </Col>
            </Row>
          </Col>
          <Col xs={1} onClick={nextPage}>Next</Col>
        </Row>
      </Container>
    </div>
  );
};
