import React, { FC, useState, useEffect } from 'react';
import { Card, Comment, CommentCreate } from '../schemas';
import { useForm } from "react-hook-form";
import { Hidden } from '../components';
import { commentTypeToString, getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';

export interface CardCommentsNewProps {
  card: Card,
  hasCommented: boolean,
  registerField: (name: string) => any,
  onSubmit: (ev: any) => any,
};

export const CardCommentsNew: FC<CardCommentsNewProps> = (props: CardCommentsNewProps) => {
  const { card, hasCommented, registerField, onSubmit } = props;
  const [submitted, setSubmitted] = useState<boolean>(false);

  const localOnSubmit = (ev: any) => {
    setSubmitted(true);
    return onSubmit(ev);
  };

  return (
    <div>
      { hasCommented ? (
        <p>Thank you for your <strong>contribution</strong>.</p>
      ) : (
        <form className={'createComment'} onSubmit={localOnSubmit}>
          <h3>Add a Comment</h3>
          <label>
            <select {...registerField("type")}>
              <option value="NEED_MET">{commentTypeToString(card, 'NEED_MET')}</option>
              <option value="NEED_NOT_MET">{commentTypeToString(card, 'NEED_NOT_MET')}</option>
              <option value="DEFINE">{commentTypeToString(card, 'DEFINE')}</option>
              <option value="THINK">{commentTypeToString(card, 'THINK')}</option>
            </select>
          </label>
          <label>
            <textarea {...registerField("data")} />
          </label>
          <label>
            {submitted ? (
              <p>Submitting...</p>
            ) : (
              <input type="submit" value="Add" />
            )}
          </label>
        </form>
    )}
    </div>
  );
};
