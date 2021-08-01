export interface CommentBase {
  cardId: number;
  type: string;
  data: string;
}

export interface CommentCreate {
}

// Room object from backend.
export interface Comment extends CommentBase {
  id: number;
  createdAt: Date;
}
