export interface CommentBase {
  cardId: number;
  type: CommentType;
  data: string;
}

export interface CommentCreate extends CommentBase {
}

export enum CommentType {
  NEED_MET = "NEED_MET",
  NEED_NOT_MET = "NEED_NOT_MET",
  DEFINE = "DEFINE",
  THINK = "THINK",
}

// Room object from backend.
export interface Comment extends CommentBase {
  id: number;
  createdAt: Date;
}
