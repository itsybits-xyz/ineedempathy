import React, { FC, useState, useEffect } from 'react';
import { Card, Comment, CommentCreate } from '../schemas';
import { Hidden } from '../components';
import { getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';
import { CardCommentsNew } from './card-comments-new';

export interface CardCommentsProps {
  card: Card,
};

export const CardComments: FC<CardCommentsProps> = (props: CardCommentsProps) => {
  const { card } = props;
  const [ hasCommented, setHasCommented ] = useState<boolean>(false);
  const [ comments, setComments ] = useState<Comment[]>([]);

  useEffect(() => {
    getComments(card).then((data) => {
      setComments(data);
    })
  }, [card, hasCommented]);

  return (
    <div role="article">
      <CardCommentsList card={card} comments={comments} />
      <CardCommentsNew
        card={card}
        hasCommented={hasCommented}
        onSubmit={() => {
          setHasCommented(true)
        }} />
    </div>
  );
};
