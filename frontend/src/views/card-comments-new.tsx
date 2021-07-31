import React, { FC, useState } from 'react';
import { CommentCreate, Card } from '../schemas';
import { useForm } from "react-hook-form";
import { commentTypeToString, createComment } from '../utils';
import { Hidden } from '../components';
import { Button, Card as CardEl } from 'react-bootstrap';

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
    <CardEl style={{ width: '35rem' }}>
      <CardEl.Body>
        <CardEl.Title>Contribute a new comment</CardEl.Title>
        { hasCommented ? (
          <p role="alert">Thank you for your <strong>contribution</strong>.</p>
        ) : (
          <form className={'createComment'} onSubmit={handleSubmit(localSubmit)}>
            <label>
              <select {...register("type")} data-testid="listbox">
                <option value="NEED_MET">{commentTypeToString(card, 'NEED_MET')}</option>
                <option value="NEED_NOT_MET">{commentTypeToString(card, 'NEED_NOT_MET')}</option>
                <option value="DEFINE">{commentTypeToString(card, 'DEFINE')}</option>
                <option value="THINK">{commentTypeToString(card, 'THINK')}</option>
              </select>
            </label>
            <label>
              <textarea {...register("data")} />
            </label>
            <label>
              {submitted ? (
                <p>Submitting...</p>
              ) : (
                <Button type="submit">Add Comment</Button>
              )}
            </label>
          </form>
        )}
      </CardEl.Body>
    </CardEl>
  );
};
