export interface RoomBase {
  name: string;
}

export interface RoomCreate {
}

// Room object from backend.
export interface Room extends RoomBase {
  id: number;
  name: string;
  createdAt: Date;
}
