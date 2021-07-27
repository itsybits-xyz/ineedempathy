import React, { FC, useState } from 'react';
import { Card, Comment } from '../schemas';
import { commentTypeToString } from '../utils';

export interface CardCommentsListProps {
  card: Card,
  comments: Comment[],
  defaultFilters: Object,
};

export const CardCommentsList: FC<CardCommentsListProps> = (props: CardCommentsListProps) => {
  const { card, comments } = props;
  const [ filters, setFilters ] = useState({
    NEED_NOT_MET: true,
    NEED_MET: true,
    DEFINE: true,
    THINK: false,
  });

  const renderButton = (name) => {
    const className = filters[name] ? 'enabled' : 'disabled'
    const onClick = () => {
      setFilters({
        ...filters,
        [name]: !filters[name],
      });
    };
    return (
      <button className={className} onClick={onClick}>{name}</button>
    );
  };

  return (
    <div>
      <div id="filters">
        { renderButton('NEED_MET') }
        { renderButton('NEED_NOT_MET') }
        { renderButton('DEFINE') }
        { renderButton('THINK') }
      </div>
      <div>
        { comments.filter((comment: Comment) => {
          return filters[comment.type];
        }).map((comment: Comment, idx: number) => {
          return (
            <div key={idx} className={'cardComment ' + comment.type} role="comment">
              <p>{commentTypeToString(card, comment.type)}</p>
              <p>{comment.data}</p>
            </div>
          );
        }) }
      </div>
    </div>
  );
};
