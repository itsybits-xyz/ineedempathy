import React, { FC } from 'react';
import { Card, Comment } from '../schemas';
import { commentTypeToString } from '../utils';

export interface CardCommentsListProps {
  card: Card,
  comments: Comment[],
};


export const CardCommentsList: FC<CardCommentsListProps> = (props: CardCommentsListProps) => {
  const { card, comments } = props;

  return (
    <div>
      { comments.map((comment: Comment, idx: number) => {
        return (
          <div key={idx} className={'cardComment ' + comment.type}>
            <p>{commentTypeToString(card, comment.type)}</p>
            <p>{comment.data}</p>
          </div>
        );
      }) }
    </div>
  );
};
