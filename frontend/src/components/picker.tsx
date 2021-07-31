import React, { FC } from 'react';
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

  if (error) {
    return (
      <Hidden error={error} />
    );
  }

  if (isPending || !data) {
    return (
      <div className="content">
        Loading...
      </div>
    );
  }

  const filterType = props.type === 'needs' ? 'need' : 'feeling';
  const cards = data.filter((card: Card) => {
    return card.type === filterType;
  });

  return (
    <div className="content fn-cards">
      <Container fluid>
        <Row>
          { cards.map((card) => {
            return (
              <Col>
                <PickerCard card={ card } />
              </Col>
            );
          }) }
        </Row>
      </Container>
    </div>
  );
};

Picker.defaultProps = defaultProps;
