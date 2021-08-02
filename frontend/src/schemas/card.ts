// Common Room attributes
export interface CardBaseImage {
  og: string;
  md: string;
  lg: string;
}

export enum CardType {
  feeling = "feeling",
  need = "need",
}

export enum CardLevel {
  intro = 1,
  beginner = 2,
  intermediate = 3,
  all = 4,
}

export interface CardBase {
  displayName: string;
  name: string;
  type: CardType;
  level: number;
  definition: string;
  definitionSource: string;
  image: CardBaseImage;
}

// Room object from backend.
export interface Card extends CardBase{
  id: number;
}
