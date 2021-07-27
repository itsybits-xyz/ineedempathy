import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsNew } from './card-comments-new';

test('submitting form invokes callback', () => {
  let called = false;
  const props: CardCommentsNewProps = {
    card<Card>: {
      name: 'compersion',
      type: 'feeling',
      textUrl: 'about:blank',
    },
    hasCommented: false,
    registerField: (name: string) => {},
    onSubmit: (ev: any) => {
      ev.preventDefault();
      called = true;
    },
  }
  render(<CardCommentsNew {...props} />);
  fireEvent.change(screen.getByRole('listbox'), { target: { value: "DEFINE" } })
  fireEvent.change(screen.getByRole('textbox'), {
    target: { value: 'princess.wiggles' }
  })
  fireEvent.click(screen.getByRole('button'))
  expect(() => screen.getByRole('button') ).toThrow();
  expect(() => screen.getByRole('alert') ).toThrow();
  expect(called).toBeTruthy();
});

test('renders submitted message', () => {
  const props: CardCommentsNewProps = {
    card<Card>: {
      name: 'compersion',
      type: 'feeling',
      textUrl: 'about:blank',
    },
    hasCommented: true,
    registerField: (name: string) => {},
    onSubmit: (ev: any) => {},
  }
  render(<CardCommentsNew {...props} />);
  expect(screen.getByRole('alert')).toBeTruthy();
});
