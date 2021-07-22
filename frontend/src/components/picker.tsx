import React, { FC, useState } from 'react';
import { Container, Col, Row } from 'react-bootstrap';
import { getCards } from '../utils/api';
import { useAsync } from 'react-async';
import { PickerCard, Hidden } from './';
import { Card } from '../schemas';

export interface PickerProps {
  type?: string;
  name?: string;
};

const defaultProps: PickerProps = {
    type: 'needs',
};

export const Picker: FC<PickerProps> = (props: PickerProps) => {
  const { data, error, isPending } = useAsync(getCards);
  const [page, setPage] = useState<number>(0);

  if (error) {
    return (
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={error} />
      </>
    );
  }

  if (isPending || !data) {
    return (
      <>
        <div className="content">
          Loading...
        </div>
      </>
    );
  }

  const filterType = props.type === 'needs' ? 'need' : 'feeling';
  const perPage = 8; // Cards displayed below
  const cards = data.filter((card: Card) => {
    return card.type === filterType;
  });
  const totalPages = Math.ceil(cards.length / perPage) - 1;
  const nextPage = () => setPage(page === totalPages ? page : page + 1);
  const prevPage = () => setPage(page === 0 ? 0 : page - 1);
  const start = page * perPage;
  const end = start + perPage;
  const displayCards = cards.slice(start, end);

  return (
    <div className="content">
      <Hidden>
        <h4>Page Debug Info</h4>
        <p>{ start }-{ end } :: {page}/{ totalPages }</p>
      </Hidden>
      <Container fluid>
        <Row>
          <Col xs={1} onClick={prevPage}>Prev</Col>
          <Col>
            <Row>
              { displayCards[0] && (
                <Col>
                  <PickerCard card={ displayCards[0] } />
                </Col>
              ) }
              { displayCards[1] && (
                <Col>
                  <PickerCard card={ displayCards[1] } />
                </Col>
              ) }
              { displayCards[2] && (
                <Col>
                  <PickerCard card={ displayCards[2] } />
                </Col>
              ) }
              { displayCards[3] && (
                <Col>
                  <PickerCard card={ displayCards[3] } />
                </Col>
              ) }
            </Row>
            <Row>
              { displayCards[4] && (
                <Col>
                  <PickerCard card={ displayCards[4] } />
                </Col>
              ) }
              { displayCards[5] && (
                <Col>
                  <PickerCard card={ displayCards[5] } />
                </Col>
              ) }
              { displayCards[6] && (
                <Col>
                  <PickerCard card={ displayCards[6] } />
                </Col>
              ) }
              { displayCards[7] && (
                <Col>
                  <PickerCard card={ displayCards[7] } />
                </Col>
              ) }
            </Row>
          </Col>
          <Col xs={1} onClick={nextPage}>Next</Col>
        </Row>
      </Container>
    </div>
  );
};

Picker.defaultProps = defaultProps;
