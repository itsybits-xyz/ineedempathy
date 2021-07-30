import React, { FC, useState, useEffect } from 'react';
import { Card, Comment, CommentCreate } from '../schemas';
import { Hidden } from '../components';
import { getComments, createComment } from '../utils';
import { CardCommentsList } from './card-comments-list';
import { CardCommentsNew } from './card-comments-new';
import { Container, Row } from 'react-bootstrap';

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
    <Container fluid>
      <Row className="justify-content-sm-center">
        { comments.length === 0 ? (
          <h3>No Comments</h3>
        ) : (
          <h4>Comments ({comments.length})</h4>
        ) }
      </Row>
      <Row className="justify-content-sm-center">
        <CardCommentsNew
          card={card}
          hasCommented={hasCommented}
          onSubmit={() => {
            setHasCommented(true)
          }} />
      </Row>
      <Row className="justify-content-sm-center">
        <CardCommentsList card={card} comments={comments} />
      </Row>
    </Container>
  );
};
