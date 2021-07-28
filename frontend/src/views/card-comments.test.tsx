import { jest } from '@jest/globals'
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
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
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  render(<CardComments card={card} />);
  const article = screen.getByRole('article');
  expect(article).toBeTruthy();
});
