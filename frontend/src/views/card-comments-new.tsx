import React, { FC, useState, useEffect } from 'react';
import { CommentCreate, Card, Comment } from '../schemas';
import { useForm } from "react-hook-form";
import { commentTypeToString, getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';
import { Hidden } from '../components';

export interface CardCommentsNewProps {
  card: Card,
  hasCommented: boolean,
  onSubmit: () => any,
};

export const CardCommentsNew: FC<CardCommentsNewProps> = (props: CardCommentsNewProps) => {
  const { card, hasCommented, onSubmit } = props;
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { register, handleSubmit } = useForm();
  const [ error, setError ] = useState(false);

  const localSubmit = (comment: CommentCreate) => {
    createComment(card, comment).then(() => {
      setSubmitted(true);
      return onSubmit();
    }).catch((er) => {
      setError(er);
    });
  };

  if (error) {
    return <Hidden error={error} />
  }

  return (
    <div>
      { hasCommented ? (
        <p role="alert">Thank you for your <strong>contribution</strong>.</p>
      ) : (
        <form className={'createComment'} onSubmit={handleSubmit(localSubmit)}>
          <h3>Add a Comment</h3>
          <label>
            <select {...register("type")} role="listbox">
              <option value="NEED_MET">{commentTypeToString(card, 'NEED_MET')}</option>
              <option value="NEED_NOT_MET">{commentTypeToString(card, 'NEED_NOT_MET')}</option>
              <option value="DEFINE">{commentTypeToString(card, 'DEFINE')}</option>
              <option value="THINK">{commentTypeToString(card, 'THINK')}</option>
            </select>
          </label>
          <label>
          <textarea role="textbox" {...register("data")} />
          </label>
          <label>
            {submitted ? (
              <p>Submitting...</p>
            ) : (
              <input role="button" type="submit" value="Add" />
            )}
          </label>
        </form>
    )}
    </div>
  );
};
