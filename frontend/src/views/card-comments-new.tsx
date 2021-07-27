import React, { FC, useState, useEffect } from 'react';
import { Card, Comment, CommentCreate } from '../schemas';
import { useForm } from "react-hook-form";
import { Hidden } from '../components';
import { getTypeString, isEmptyValue, getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';

export interface CardCommentsNewProps {
  card: Card,
  hasCommented: boolean,
  registerField: (name: string) => any,
  onSubmit: () => any,
};

export const CardCommentsNew: FC<CardCommentsNewProps> = (props: CardCommentsNewProps) => {
  const { card, hasCommented, registerField, onSubmit } = props;

  return (
    <div>
      { hasCommented ? (
        <p>Thank you for your <strong>contribution</strong>.</p>
      ) : (
        <form className={'createComment'} onSubmit={onSubmit}>
          <h3>Add a Comment</h3>
          <label>
            <select {...registerField("type")}>
              <option value="NEED_MET">{getTypeString(card, 'NEED_MET')}</option>
              <option value="NEED_NOT_MET">{getTypeString(card, 'NEED_NOT_MET')}</option>
              <option value="DEFINE">{getTypeString(card, 'DEFINE')}</option>
              <option value="THINK">{getTypeString(card, 'THINK')}</option>
            </select>
          </label>
          <label>
            <textarea {...registerField("data")} />
          </label>
          <label>
            <input type="submit" value="Add" />
          </label>
        </form>
    )}
    </div>
  );
};
