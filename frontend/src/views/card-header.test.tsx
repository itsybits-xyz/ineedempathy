import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardHeader } from './card-header';

test('renders card header', () => {
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
  render(<CardHeader card={card} />);
  const img = screen.getByRole('img');
  expect(img).toHaveAttribute('alt');
  expect(() => screen.getByRole('alert') ).toThrow();
});

test('renders error header', () => {
  const card: Card = {
    id: 1,
    displayName: 'Compersion',
    name: 'compersion',
    type: 'feeling',
    level: 1,
    definition: 'meow',
    definitionSource: 'meow',
    image: {
      og: 'foo.png',
      lg: 'foo.png',
      md: 'foo.png',
    },
  }
  render(<CardHeader card={card} />);
  const img = screen.getByRole('img');
  fireEvent.error(img);
  const alert = screen.getByRole('alert');
  expect(alert).toBeTruthy();
});
