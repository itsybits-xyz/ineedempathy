import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardHeader } from './card-header';

test('renders card header', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  render(<CardHeader card={card} />);
  const img = screen.getByRole('img');
  expect(img).toHaveAttribute('alt');
  expect(() => screen.getByRole('alert') ).toThrow();
});

test('renders error header', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'foo.png',
  }
  render(<CardHeader card={card} />);
  const img = screen.getByRole('img');
  fireEvent.error(img);
  const alert = screen.getByRole('alert');
  expect(alert).toBeTruthy();
});
