import React from 'react';
import { act, render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsNew } from './card-comments-new';
import { createComment } from '../utils'

jest.mock('../utils', () => {
  return {
    commentTypeToString: () => 'meow',
    createComment: jest.fn(),
  };
});

describe('happy paths', () => {
  beforeEach(() => {
    createComment.mockImplementation(() => {
      return Promise.resolve();
    });
  });
  test('submitting form invokes callback', async () => {
    let called = false;
    const props: CardCommentsNewProps = {
      card<Card>: {
        name: 'compersion',
        type: 'feeling',
        textUrl: 'about:blank',
      },
      hasCommented: false,
      onSubmit: () => {
        called = true;
      },
    }
    await act(async () => {
      render(<CardCommentsNew {...props} />);
      fireEvent.change(screen.getByRole('listbox'), { target: { value: "DEFINE" } });
      fireEvent.change(screen.getByRole('textbox'), {
        target: { value: 'princess.wiggles' }
      });
      fireEvent.click(screen.getByText('Add'));
    });
    expect(() => screen.getByText('Add')).toThrow();
    expect(called).toBeTruthy(); });

  test('renders submitted message', () => {
    const props: CardCommentsNewProps = {
      card<Card>: {
        name: 'compersion',
        type: 'feeling',
        textUrl: 'about:blank',
      },
      hasCommented: true,
      onSubmit: (ev: any) => {},
    }
    act(() => {
      render(<CardCommentsNew {...props} />);
      expect(screen.getByRole('alert')).toBeTruthy();
    });
  });
});

describe('error cases', () => {
  beforeEach(() => {
    createComment.mockImplementation(() => {
      return Promise.reject();
    });
  });

  test('handles error on submit', async () => {
    let called = false;
    const props: CardCommentsNewProps = {
      card<Card>: {
        name: 'compersion',
        type: 'feeling',
        textUrl: 'about:blank',
      },
      hasCommented: false,
      onSubmit: () => { called = true },
    }
    await act(async () => {
      render(<CardCommentsNew {...props} />);
      fireEvent.change(screen.getByRole('listbox'), { target: { value: "DEFINE" } });
      fireEvent.change(screen.getByRole('textbox'), {
        target: { value: 'princess.wiggles' }
      });
      fireEvent.click(screen.getByText('Add'));
    });
    expect(called).toBeFalsy();
    expect(screen.getByText('Add')).toBeTruthy();
  });
});
