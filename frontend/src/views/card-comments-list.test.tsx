import React from 'react';
import { render, screen } from '@testing-library/react';
import { Card, Comment } from '../schemas';
import { CardCommentsList } from './card-comments-list';

test('renders comments list', () => {
  const card: Card = {
    name: 'compersion',
    type: 'feeling',
    textUrl: 'about:blank',
  }
  const comments: Comment[] = [
    { cardId: 1, type: 'FEELING_MET', data: 'princess.wiggles' },
    { cardId: 1, type: 'FEELING_MET', data: 'princess.wiggles' },
  ]
  render(<CardCommentsList card={card} comments={comments} />);
  return screen.findAllByRole('comment').then((renderedComments) => {
    expect(renderedComments).toHaveLength(2)
  });
});
