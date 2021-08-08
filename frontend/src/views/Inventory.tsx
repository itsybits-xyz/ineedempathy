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
              <p>
                Feelings are what we feel inside of our body, these feelings
                suggest we have met or unmet needs.
              </p>
            </>
          ) : (
            <>
              <h2>Need Cards</h2>
              <p>
                Every action you take is an attempt to meet a need. Waving your
                hand while you talk, every word you say, when you move or don't
                move.
              </p>
            </>
          ) }
          <p>
            You can browse the cards below, if you'd like to be presented with
            less cards, try changing the level from the dropdown above. If you
            want more information about a card, click on the card to go to the
            Card Page, which has a definition and comments people have made.
          </p>
          <Picker type={type} />
        </Container>
      </div>
    </>
  );
};
