import { CommentType, Card } from '../schemas';
import shuffle from 'lodash.shuffle';

export * from './api';

const colors = [
  'pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple',
  'aqua', 'black', 'magenta', 'violet', 'opal', 'seafoam', 'coral',
];
const animals = [
  'whale', 'giraffe', 'turtle', 'jellyfish', 'dog', 'bison', 'cat',
  'hamster', 'sugar-glider', 'rabbit', 'gecko', 'mouse', 'moth', 'hedgehog',
];
export function generateName(): string {
  const color = shuffle(colors)[0];
  const animal = shuffle(animals)[0];
  const number = Math.round(Math.random() * 1000);

  return `${color}-${animal}-${number}`;
}

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
