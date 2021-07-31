// Common Room attributes
export interface CardBase {
  displayName: string;
  name: string;
  type: string;
  level: number;
  definition: string;
  definitionSource: string;
  blankUrl: string;
  textUrl: string;
}

// Room object from backend.
export interface Card extends CardBase{
  id: number;
}
