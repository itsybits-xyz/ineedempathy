// Common Room attributes
export interface CardBaseImage {
  og: string;
  md: string;
  lg: string;
}

export interface CardBase {
  displayName: string;
  name: string;
  type: string;
  level: number;
  definition: string;
  definitionSource: string;
  image: CardBaseImage;
}

// Room object from backend.
export interface Card extends CardBase{
  id: number;
}
