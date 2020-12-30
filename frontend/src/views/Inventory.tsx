import React, { FC } from 'react';
import { Container } from 'react-bootstrap';
import { Picker } from '../components';

export interface InventoryProps {
  match: {
    params: {
      type: string
    }
  }
}

export const Inventory: FC<InventoryProps> = (props: InventoryProps) => {
  const type = props.match.params.type;
  const isFeelings = type === 'feelings';
  return (
    <>
      <div className="content">
        <Container fluid>
          <h2>{ isFeelings ? 'Feelings' : 'Needs' } Cards</h2>
          <p>Short description</p>
          <Picker type={type} />
        </Container>
      </div>
    </>
  );
};
