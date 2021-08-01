import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsList } from './card-comments-list';

test('renders comments list', () => {
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
  const comments: Comment[] = [
    { id: 1, cardId: 1, type: 'NEED_MET', data: 'princess.wiggles', createdAt: new Date() },
    { id: 2, cardId: 1, type: 'NEED_NOT_MET', data: 'princess.wiggles', createdAt: new Date() },
    { id: 3, cardId: 1, type: 'DEFINE', data: 'princess.wiggles', createdAt: new Date() },
    { id: 4, cardId: 1, type: 'THINK', data: 'princess.wiggles', createdAt: new Date() },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(4)
  });
});

test('toggle all the filters', () => {
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
  const comments: Comment[] = [
    { id: 1, cardId: 1, type: 'NEED_MET', data: 'princess.wiggles', createdAt: new Date() },
    { id: 2, cardId: 1, type: 'NEED_NOT_MET', data: 'princess.wiggles', createdAt: new Date() },
    { id: 3, cardId: 1, type: 'DEFINE', data: 'princess.wiggles', createdAt: new Date() },
    { id: 4, cardId: 1, type: 'THINK', data: 'princess.wiggles', createdAt: new Date() },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(4);
  }).then(() => {
    fireEvent.click(screen.getByText('Thoughts'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(3);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('Definitions'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(2);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('Unmet Needs'));
    return screen.findAllByRole('comment').then((renderedComments) => {
      expect(renderedComments).toHaveLength(1);
    });
  }).then(() => {
    fireEvent.click(screen.getByText('Met Needs'));
    return screen.findAllByRole('comment').then(() => {
      // Raise exception, there should be no comments
      expect(false).toBeTruthy();
    }, () => {
      // Assert no comments
      expect(true).toBeTruthy();
    });
  });
});
