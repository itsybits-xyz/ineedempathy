import React, { FC, useState, useEffect } from 'react';
import { BACKEND_URL } from '../config';
import { Container, Col, Row } from 'react-bootstrap';
import { getCards, getComments, createComment } from '../utils/api';
import { useAsync } from 'react-async';
import { Hidden } from '../components';
import { Card, Comment, CommentCreate } from '../schemas';
import { useForm } from "react-hook-form";

export interface CardPageProps {
  match: {
    params: {
      type: string
      name: string
    }
  }
};

function getTypeString(card:Card, commentType:string) {
  const cardName:string = card.name;
  switch(commentType) {
    case 'NEED_MET':
      return `My need for ${cardName} was met when..`;
    case 'NEED_NOT_MET':
      return `My need for ${cardName} was not met when..`;
    case 'DEFINE':
      return `I define ${cardName} as..`;
    case 'THINK':
      return `My thoughts on ${cardName} are..`;
  }
}

export const CardPage: FC<CardPageProps> = (props: CardPageProps) => {
  const { name } = props.match.params;
  const { data: cardData, error: cardError, isPending: loadingCards } = useAsync(getCards);
  const [ commentData, setCommentData ] = useState<Comment[]>([]);
  const [ hasCommented, setHasCommented ] = useState<boolean>(false);
  const { register, handleSubmit, formState: { errors: commentError } } = useForm();

  useEffect(() => {
    getComments(name).then((data) => {
      setCommentData(data);
    })
  }, [name, hasCommented]);


  const isEmptyValue = (val:any) => {
    if (!val) { return true; }
    if (Object.keys(val).length === 0) { return true; }
    return false
  };

  if (!isEmptyValue(cardError) || !isEmptyValue(commentError)) {
    return (
      <>
        <p>An unexpected error occured.</p>
        <Hidden error={cardError || commentError} />
      </>
    );
  }

  if (loadingCards || !cardData) {
    return (
      <>
        <div className="content">
          Loading...
        </div>
      </>
    );
  }

  const cards: Card[] = cardData.filter((card: Card) => {
    return card.name === name;
  });

  const card: Card = cards[0];

  if (!card) {
    return (
      <>
        <div className="content">
          Card not found.
        </div>
      </>
    );
  }

  const onSubmit = (comment: CommentCreate) => {
    createComment(card, comment).then(() => {
      setHasCommented(true);
    });
  };

  return (
    <>
      <div>
        <img alt={card.name} width={200} src={BACKEND_URL + card.textUrl} />
      </div>
      <div>
        { commentData.map((comment: Comment) => {
          return (
            <div className={'cardComment ' + comment.type}>
              <p>{getTypeString(card, comment.type)}</p>
              <p>{comment.data}</p>
            </div>
          );
        }) }
      </div>
      <div>
        { hasCommented ? (
          <p>Thank you for your <strong>contribution</strong>.</p>
        ) : (
          <form className={'createComment'} onSubmit={handleSubmit(onSubmit)}>
            <h3>Add a Comment</h3>
            <label>
              <select {...register("type")}>
                <option value="NEED_MET">{getTypeString(card, 'NEED_MET')}</option>
                <option value="NEED_NOT_MET">{getTypeString(card, 'NEED_NOT_MET')}</option>
                <option value="DEFINE">{getTypeString(card, 'DEFINE')}</option>
                <option value="THINK">{getTypeString(card, 'THINK')}</option>
              </select>
            </label>
            <label>
              <textarea {...register("data", {})} />
            </label>
            <label>
              <input type="submit" value="Add" />
            </label>
          </form>
      )}
      </div>
    </>
  );

};
