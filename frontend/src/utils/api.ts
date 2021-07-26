import { BACKEND_URL } from '../config';
import { Card, Room, User, UserCreate, RoomCreate } from '../schemas';
import {PromiseFn} from 'react-async';

function http<T>(path: string, authenticated: boolean = true, config: RequestInit): Promise<T> {
  const headers = new Headers();
  headers.append('Content-Type', 'application/json');
  const request = new Request(path, {headers, ...config});
  return fetch(request).then((response) => {
    return response.json();
  });
}

export function get<T>(path: string, authenticated: boolean = true, config?: RequestInit): Promise<T> {
  const init = { method: 'get', ...config };
  return http<T>(path, authenticated, init);
}

export function post<T, U>(
  path: string,
  body: T,
  authenticated: boolean = true,
  config?: RequestInit
): Promise<U> {
  const init = { method: 'post', body: JSON.stringify(body), ...config };
  return http<U>(path, authenticated, init);
}

export function put<T, U>(
  path: string,
  body: T,
  authenticated: boolean = true,
  config?: RequestInit
): Promise<U> {
  const init = { method: 'put', body: JSON.stringify(body), ...config };
  return http<U>(path, authenticated, init);
}

export const getMessage = async () => {
  const response = await fetch(BACKEND_URL);
  const data = await response.json();
  if (data.msg) {
    return data.msg;
  }
  return Promise.reject('Failed to get message from backend');
};

export const getCards = () => {
  return get<Card[]>(`${BACKEND_URL}/cards`);
};

export const getCard = (name: string) => {
  return get<Card>(`${BACKEND_URL}/cards/${name}`);
};

export const getRooms = () => {
  return get<Room[]>(`${BACKEND_URL}/rooms`);
};

export const getRoom: PromiseFn<Room> = ({roomId}) => {
  return get<Room>(`${BACKEND_URL}/rooms/${roomId}`);
};

export const createUser = (roomName: string) => {
  return post<UserCreate, User>(`${BACKEND_URL}/rooms/${roomName}/user`, {});
};

export const createRoom = () => {
  return post<RoomCreate, Room>(`${BACKEND_URL}/rooms`, {} as RoomCreate);
};
