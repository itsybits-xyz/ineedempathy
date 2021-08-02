import React, { FC, useState } from 'react';
import { Card, Comment } from '../schemas';
import { ClickSound } from '../components';
import { commentTypeToString } from '../utils';
import { Badge, Card as CardEl, Container, Row, Button, ButtonGroup } from 'react-bootstrap';
import { MdSearch } from 'react-icons/md';

export interface CardCommentsListProps {
  card: Card,
  comments: Comment[],
};

export const CardCommentsList: FC<CardCommentsListProps> = (props: CardCommentsListProps) => {
  const { card, comments } = props;
  const [ filters, setFilters ] = useState([
    { key: 'NEED_MET', name: 'Met Needs', active: true, variant: 'primary' },
    { key: 'NEED_NOT_MET', name: 'Unmet Needs', active: true, variant: 'danger' },
    { key: 'DEFINE', name: 'Definitions', active: true, variant: 'info' },
    { key: 'THINK', name: 'Thoughts', active: true, variant: 'secondary' },
  ]);

  if (comments.length === 0) {
    return null;
  }

  const filteredComments = comments.filter((comment: Comment) => {
    const filter = filters.find((filter) => {
      return filter.key === comment.type
    });
    return filter && filter.active;
  })

  return (
    <Container fluid>
      <Row className="justify-content-sm-center">
        <ButtonGroup>
          { filters.map((filter, idx) => (
              <ClickSound key={idx}>
                <Button
                  onClick={() => {
                    const newFilters = [...filters];
                    newFilters[idx] = Object.assign({}, filter, {
                      active: !filter.active,
                    });
                    setFilters(newFilters);
                    document.activeElement?.blur();
                  }}
                  value={filter.key}
                  variant={filter.variant}
                  size="md"
                  type="checkbox"
                  active={filter.active}
                  checked={filter.active}>
                  {filter.name}
                </Button>
              </ClickSound>
          )) }
        </ButtonGroup>
      </Row>
      <Container fluid>
        { filteredComments.length === 0 ? (
          <Row className="justify-content-sm-center">
            <CardEl role="comment" style={{ width: '35rem' }}>
              <CardEl.Body>
                <CardEl.Title>
                  <MdSearch size={36} />
                </CardEl.Title>
                <CardEl.Title>
                  No comments found.
                </CardEl.Title>
                <CardEl.Title>
                  Try adjusting your filters, or <strong>contributing</strong> your own.
                </CardEl.Title>
              </CardEl.Body>
            </CardEl>
          </Row>
        ) : (
          filteredComments.map((comment: Comment, idx: number) => {
            const filter = filters.find((filter) => {
              return filter.key === comment.type
            });
            return (
              <Row key={idx} className="justify-content-sm-center">
                <CardEl
                  role="comment"
                  style={{ width: '35rem' }}>
                  <CardEl.Body>
                    <CardEl.Title>
                      <Badge pill variant={filter?.variant}>
                        &nbsp;
                      </Badge>
                      {' '}
                      {commentTypeToString(card, comment.type)}
                    </CardEl.Title>
                    <CardEl.Text>{comment.data}</CardEl.Text>
                  </CardEl.Body>
                </CardEl>
              </Row>
            );
          })
        )}
      </Container>
    </Container>
  );
};
