import { jest } from '@jest/globals'
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardComments } from './card-comments';

test('renders card comments', () => {
  jest.mock('../utils', () => {
    return {
      getComments: () => {
        return Promise.resolve([]);
      },
      createComments: () => {
        return Promise.resolve();
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
  expect(screen.getByText('Add')).toBeTruthy();
});

test('renders onSubmit error', () => {
  // Setup
  jest.mock('../utils', () => {
    return {
      getComments: () => {
        return Promise.resolve([]);
      },
      createComments: () => {
        return Promise.reject(new Error('princess.wiggles'));
      },
    };
  });
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  render(<CardComments card={card} />);

  // Action
  fireEvent.click(screen.getByText('Add'));

  // Assertion
  const article = screen.getByRole('article');
  expect(article).toBeTruthy();
  expect(() => screen.getByText('Add') ).toThrow();
});
