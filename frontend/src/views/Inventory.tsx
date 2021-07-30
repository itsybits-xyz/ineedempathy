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
  const type: string = String(props.match.params.type);
  const isFeelings = type === 'feelings';
  return (
    <>
      <div className="content">
        <Container fluid>
          { isFeelings ? (
            <>
              <h2>Feeling Cards</h2>
              <p>Feelings are what we feel inside of our body, these feelings suggest we have met or unmet needs.</p>
            </>
          ) : (
            <>
              <h2>Need Cards</h2>
              <p>Every action you take is an attempt to meet a need. Waving your hand while you talk, every word you say, when you move or don't move.</p>
            </>
          ) }
          <Picker type={type} />
        </Container>
      </div>
    </>
  );
};
