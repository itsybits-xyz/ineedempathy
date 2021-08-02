import { CommentType, Card } from '../schemas';

export * from './api';

export function commentTypeToString(card:Card, commentType:CommentType) {
  const cardName:string = card.displayName;
  switch(commentType) {
    case CommentType.NEED_MET:
      switch (card.type) {
        case 'feeling':
          return `When I felt ${cardName} the needs that were met were..`;
        case 'need':
          return `My need for ${cardName} was met when..`;
        default:
          return '';
      }
    case CommentType.NEED_NOT_MET:
      switch (card.type) {
        case 'feeling':
          return `When I felt ${cardName} the needs that were not met were..`;
        case 'need':
          return `My need for ${cardName} was not met when..`;
        default:
          return '';
      }
    case CommentType.DEFINE:
      return `I define ${cardName} as..`;
    case CommentType.THINK:
      return `My thoughts on ${cardName} are..`;
    default:
      return '';
  }
}
