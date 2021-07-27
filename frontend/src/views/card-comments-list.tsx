import React, { FC } from 'react';
import { Card, Comment } from '../schemas';
import { getTypeString } from '../utils';

export interface CardCommentsListProps {
  card: Card,
  comments: Comment[],
};


export const CardCommentsList: FC<CardCommentsListProps> = (props: CardCommentsListProps) => {
  const { card, comments } = props;

  return (
    <div>
      { comments.map((comment: Comment) => {
        return (
          <div className={'cardComment ' + comment.type}>
            <p>{getTypeString(card, comment.type)}</p>
            <p>{comment.data}</p>
          </div>
        );
      }) }
    </div>
  );
};
