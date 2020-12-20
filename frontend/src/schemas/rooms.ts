// Common Room attributes
export interface RoomBase {
  name: string;
  type: number;
}

export interface RoomCreate extends RoomBase {
}

// Room object from backend.
export interface Room extends RoomBase{
  id: number;
  createdAt: Date;
}
