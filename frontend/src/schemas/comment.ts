export interface CommentBase {
  name: string;
}

export interface CommentCreate {
  card_id: number;
  type: string;
  data: string;
}

// Room object from backend.
export interface Comment extends CommentBase {
  id: number;
  card_id: number;
  type: string;
  data: string;
  createdAt: Date;
}
