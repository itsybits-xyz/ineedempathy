import { CommentType, Card } from '../schemas';

export * from './api';

const colors = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple'];
const animals = ['whale', 'giraffe', 'turtle', 'jellyfish', 'dog', 'bison', 'cat'];
export function generateName(): string {
  const randomSort = (one: any, two: any) => {
    if (Math.round(Math.random() * 1000) % 2) return 1;
    if (Math.round(Math.random() * 1000) % 2) return -1;
    return 0;
  }

  const color = colors.sort(randomSort)[0];
  const animal = animals.sort(randomSort)[0];
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
