import { Card } from '../schemas';

export * from './api';

export function commentTypeToString(card:Card, commentType:string) {
  const cardName:string = card.name;
  switch(commentType) {
    case 'NEED_MET':
      switch (card.type) {
        case 'feeling':
          return `When I felt ${cardName} the needs that were met were..`;
        case 'need':
          return `My need for ${cardName} was met when..`;
      }
    case 'NEED_NOT_MET':
      switch (card.type) {
        case 'feeling':
          return `When I felt ${cardName} the needs that were not met were..`;
        case 'need':
          return `My need for ${cardName} was not met when..`;
      }
    case 'DEFINE':
      return `I define ${cardName} as..`;
    case 'THINK':
      return `My thoughts on ${cardName} are..`;
  }
}
