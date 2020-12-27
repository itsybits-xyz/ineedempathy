// Common Room attributes
export interface UserBase {
  id: number;
  name: string;
  roomId: string;
}

export interface UserCreate {
}

// Room object from backend.
export interface User extends UserBase{
}
