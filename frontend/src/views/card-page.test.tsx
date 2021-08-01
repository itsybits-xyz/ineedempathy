import { jest } from '@jest/globals'
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardPage } from './card-page';
import { act } from "react-dom/test-utils";

test('shows loading screen', () => {
  jest.mock('../utils', () => {
    return {
      getCard: (name: string) => {
        return Promise.resolve({});
      },
    };
  });
  const props: CardPageProps = { match: { params: {
    type: 'feeling',
    name: 'compersion'
  }}};
  render(<CardPage {...props} />);
  expect(screen.getByRole('alert')).toBeTruthy();
});

test('renders card page', () => {
  jest.mock('../utils', () => {
    return {
      getCard: (name: string) => {
        return Promise.resolve({
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
        });
      },
    };
  });
  const props: CardPageProps = { match: { params: {
    type: 'feeling',
    name: 'compersion'
  }}};
  return act(() => {
    return Promise.resolve(render(<CardPage {...props} />));
  }).then(() => {
    expect(() => screen.getByRole('alert') ).toThrow();
  });
});

test('renders error', () => {
  jest.mock('../utils', () => {
    return {
      getCard: (name: string) => {
        return Promise.reject(new Error('princess.wiggles'));
      },
    };
  });
  const props: CardPageProps = { match: { params: {
    type: 'feeling',
    name: 'compersion'
  }}};
  return act(() => {
    return Promise.resolve(render(<CardPage {...props} />));
  }).then(() => {
    expect(screen.getByRole('alert')).toBeTruthy();
  });
});

