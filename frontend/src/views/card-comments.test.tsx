import { jest } from '@jest/globals'
import React from 'react';
import { act, render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardComments } from './card-comments';

test('renders card comments', () => {
  jest.mock('../utils', () => {
    return {
      getComments: () => {
        return Promise.resolve([1, 2, 3]);
      },
    };
  });
  const card: Card = {
    id: 1,
    displayName: 'Compersion',
    name: 'compersion',
    type: 'feeling',
    level: 1,
    definition: 'meow',
    definitionSource: 'meow',
    image: {
      og: 'about:blank',
      lg: 'about:blank',
      md: 'about:blank',
    },
  }
  render(<CardComments card={card} />);
  const title = screen.getByText('No Comments');
  expect(title).toBeTruthy();
});
