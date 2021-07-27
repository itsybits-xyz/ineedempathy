import React, { FC, useState, useEffect } from 'react';
import { BACKEND_URL } from '../config';
import { Container, Col, Row } from 'react-bootstrap';
import { getCards, getComments, createComment } from '../utils/api';
import { useAsync } from 'react-async';
import { Hidden } from '../components';
import { Card, Comment, CommentCreate } from '../schemas';

export interface CardPageProps {
  match: {
    params: {
      type: string
      name: string
    }
  }
};

export const CardPage: FC<CardPageProps> = (props: CardPageProps) => {
  const { name } = props.match.params;
  const { data: cardData, error: cardError, isPending: loadingCards } = useAsync(getCards);
  const [ type, setType ] = useState<string>('THINK');
  const [ data, setData ] = useState<string>('');
  const [ commentData, setCommentData ] = useState<Comment[]>([]);
  const [ commentError, setCommentError ] = useState();
  const [ createdComment, setCreatedComment ] = useState<boolean>(false);

  useEffect(() => {
    getComments(name).then((data) => {
      setCommentData(data);
    }).catch((er) => {
      setCommentError(er);
    });
  });

  if (cardError || commentError) {
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

  const handleCreateComment = (ev: any) => {
    const comment: CommentCreate = {
      card_id: card.id,
      type: type,
      data: data,
    }
    createComment(comment).then(() => {
      setCreatedComment(true);
    });
  };

  return (
    <>
      <div>
        <img alt={card.name} width={200} src={BACKEND_URL + card.textUrl} />
      </div>
      <div>
        { JSON.stringify(commentData) }
      </div>
      <div>
        { createdComment ? (
          <p>Thank you for your <strong>contribution</strong>.</p>
        ) : (
          <>
            <select value={type} onChange={(e) => { setType(e.target.value) }}>
              <option value="NEED_MET">NEED_MET</option>
              <option value="NEED_NOT_MET">NEED_NOT_MET</option>
              <option value="DEFINE">DEFINE</option>
              <option value="THINK">THINK</option>
            </select>
            <textarea value={data} onChange={(e) => { setData(e.target.value) }} />
            <button onClick={handleCreateComment}>Add</button>
          </>
      )}
      </div>
    </>
  );

};
