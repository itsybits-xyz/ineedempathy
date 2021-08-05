import React from 'react';
import { act, render, screen, fireEvent, createEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsNewProps, CardCommentsNew } from './card-comments-new';
import { createComment } from '../utils'


const change = async (el: HTMLElement, value: string) => {
  const changeEvent = createEvent.change(el, {
    target: { value: value },
  });
  changeEvent.inputType = 'insertText';
  act(() => {
    el.dispatchEvent(changeEvent);
  });
}

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
      },
      hasCommented: false,
      onSubmit: () => {
        called = true;
      },
    }
    render(<CardCommentsNew {...props} />);
    await act(async () => {
      await change(screen.getByRole('textbox'), 'princess.wiggles');
      fireEvent.click(screen.getByText('Add Comment'));
    });
    expect(() => screen.getByText('Add Comment')).toThrow();
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
      onSubmit: (ev: any) => {},
    }
    render(<CardCommentsNew {...props} />);
    expect(screen.getByRole('alert')).toBeTruthy();
  });
});

describe('error cases', () => {
  beforeEach(() => {
    createComment.mockImplementation(() => {
      return Promise.reject();
    });
  });

  test('handles empty comment on submit', async () => {
    let called = false;
    const props: CardCommentsNewProps = {
      card<Card>: {
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
      },
      hasCommented: false,
      onSubmit: () => { called = true },
    }
    render(<CardCommentsNew {...props} />);
    await act(async () => {
      fireEvent.click(screen.getByText('Add Comment'));
    });
    expect(screen.getByTestId('nobody-error')).toBeTruthy();
    expect(called).toBeFalsy();
  });

  test('handles error on submit', async () => {
    let called = false;
    const props: CardCommentsNewProps = {
      card<Card>: {
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
      },
      hasCommented: false,
      onSubmit: () => { called = true },
    }
    await act(async () => {
      render(<CardCommentsNew {...props} />);
      await change(screen.getByRole('textbox'), 'princess.wiggles');
      fireEvent.click(screen.getByText('Add Comment'));
      expect(called).toBeFalsy();
      expect(screen.getByText('Add Comment')).toBeTruthy();
    });
  });
});
