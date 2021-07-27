import { Card } from '../schemas';

export * from './api';

export const isEmptyValue = (val:any) => {
  if (!val) { return true; }
  if (Object.keys(val).length === 0) { return true; }
  return false
};

export function getTypeString(card:Card, commentType:string) {
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
