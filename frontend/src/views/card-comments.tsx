import React, { FC, useState, useEffect } from 'react';
import { Card, Comment, CommentCreate } from '../schemas';
import { useForm } from "react-hook-form";
import { Hidden } from '../components';
import { getTypeString, isEmptyValue, getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';
import { CardCommentsNew } from './card-comments-new';

export interface CardCommentsProps {
  card: Card,
};

export const CardComments: FC<CardCommentsProps> = (props: CardCommentsProps) => {
  const { card } = props;
  const [ error, setError ] = useState();
  const [ hasCommented, setHasCommented ] = useState<boolean>(false);
  const { register, handleSubmit, formState: { errors: commentError } } = useForm();
  const [ comments, setComments ] = useState<Comment[]>([]);

  useEffect(() => {
    getComments(card).then((data) => {
      setComments(data);
    }).catch((er) => {
      setError(er);
    });
  }, [card, hasCommented]);

  const onSubmit = handleSubmit((comment: CommentCreate) => {
    createComment(card, comment).then(() => {
      setHasCommented(true);
    });
  });

  if (!isEmptyValue(error)) {
    return (
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={error} />
      </>
    );
  }

  return (
    <>
      <CardCommentsList card={card} comments={comments} />
      <CardCommentsNew
        card={card}
        hasCommented={hasCommented}
        registerField={(name: any) => register(name)}
        onSubmit={onSubmit} />
    </>
  );
};
