// Common Room attributes
export type RoomType = "singleplayer" | "multiplayer" | "public-multiplayer";

export interface RoomBase {
  name: string;
  type: RoomType;
}

export interface RoomCreate {
  type: RoomType;
}

// Room object from backend.
export interface Room extends RoomBase {
  id: number;
  name: string;
  type: RoomType;
  createdAt: Date;
}
