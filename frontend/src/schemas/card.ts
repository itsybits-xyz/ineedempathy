// Common Room attributes
export interface CardBase {
  name: string;
  type: string;
  blankUrl: string;
  textUrl: string;
}

// Room object from backend.
export interface Card extends CardBase{
  id: number;
}
