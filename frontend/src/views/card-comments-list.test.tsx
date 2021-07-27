import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsList } from './card-comments-list';

test('renders comments list', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  const comments: Comment[] = [
    { cardId: 1, type: 'NEED_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'NEED_MET', data: 'princess.wiggles' },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(2)
  });
});

test('accepts default filters', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  const comments: Comment[] = [
    { cardId: 1, type: 'NEED_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'NEED_NOT_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'DEFINE', data: 'princess.wiggles' },
    { cardId: 1, type: 'THINK', data: 'princess.wiggles' },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(3)
  });
});

test('accepts default filters', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  const comments: Comment[] = [
    { cardId: 1, type: 'NEED_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'NEED_NOT_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'DEFINE', data: 'princess.wiggles' },
    { cardId: 1, type: 'THINK', data: 'princess.wiggles' },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(3);
  }).then(() => {
    fireEvent.click(screen.getByText('THINK'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(4);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('THINK'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(3);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('DEFINE'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(2);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('NEED_NOT_MET'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(1);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('NEED_MET'));
    return screen.findAllByRole('comment').then(() => {
      // Raise exception, there should be no comments
      expect(false).toBeTruthy();
    }, () => {
      // Assert no comments
      expect(true).toBeTruthy();
    });
  });
});
