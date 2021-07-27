export interface CommentBase {
  name: string;
}

export interface CommentCreate {
  cardId: number;
  type: string;
  data: string;
}

// Room object from backend.
export interface Comment extends CommentBase {
  id: number;
  cardId: number;
  type: string;
  data: string;
  createdAt: Date;
}
