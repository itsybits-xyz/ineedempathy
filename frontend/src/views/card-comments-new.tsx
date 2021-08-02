import React, { FC, useState } from 'react';
import { CommentCreate, CommentType, Card } from '../schemas';
import { commentTypeToString, createComment } from '../utils';
import { ClickSound, Hidden } from '../components';
import { Col, Dropdown, Row, Button, Card as CardEl } from 'react-bootstrap';

export interface CardCommentsNewProps {
  card: Card,
  hasCommented: boolean,
  onSubmit: () => any,
};

export const CardCommentsNew: FC<CardCommentsNewProps> = (props: CardCommentsNewProps) => {
  const { card, hasCommented, onSubmit } = props;
  const [ submitted, setSubmitted ] = useState<boolean>(false);
  const [ type, setType ] = useState<CommentType>(CommentType.NEED_MET);
  const [ data, setData ] = useState<string>('');
  const [ error, setError ] = useState(false);

  const localSubmit = () => {
    const comment: CommentCreate = {
      cardId: card.id,
      type: type,
      data: data,
    };
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
      <CardEl.Body className="createComment">
        <CardEl.Title>Contribute a new comment</CardEl.Title>
        { hasCommented ? (
          <p role="alert">Thank you for your <strong>contribution</strong>.</p>
        ) : (
          <>
            <Row>
              <ClickSound>
                <Col>
                  <Dropdown>
                    <Dropdown.Toggle variant="success">
                      { commentTypeToString(card, type) }
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      <Dropdown.Item
                        active={type === CommentType.NEED_MET}
                        onClick={() => setType(CommentType.NEED_MET)}>
                        { commentTypeToString(card, CommentType.NEED_MET) }
                      </Dropdown.Item>
                      <Dropdown.Item
                        active={type === CommentType.NEED_NOT_MET}
                        onClick={() => setType(CommentType.NEED_NOT_MET)}>
                        { commentTypeToString(card, CommentType.NEED_NOT_MET) }
                      </Dropdown.Item>
                      <Dropdown.Item
                        active={type === CommentType.DEFINE}
                        onClick={() => setType(CommentType.DEFINE)}>
                        { commentTypeToString(card, CommentType.DEFINE) }
                      </Dropdown.Item>
                      <Dropdown.Item
                        active={type === CommentType.THINK}
                        onClick={() => setType(CommentType.THINK)}>
                        { commentTypeToString(card, CommentType.THINK) }
                      </Dropdown.Item>
                    </Dropdown.Menu>
                  </Dropdown>
                </Col>
              </ClickSound>
            </Row>
            <Row>
              <textarea onChange={(e) => setData(e.target.value)}>{data}</textarea>
            </Row>
            <Row>
              {submitted ? (
                <p>Submitting...</p>
              ) : (
                <ClickSound>
                  <Button type="submit" onClick={localSubmit}>Add Comment</Button>
                </ClickSound>
              )}
            </Row>
          </>
        )}
      </CardEl.Body>
    </CardEl>
  );
};
