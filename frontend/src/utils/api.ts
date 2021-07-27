import { BACKEND_URL } from '../config';
import { Card, Comment, CommentCreate, Room, RoomCreate } from '../schemas';
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

export const createRoom = () => {
  return post<RoomCreate, Room>(`${BACKEND_URL}/rooms`, {} as RoomCreate);
};

export const getComments = (card: Card) => {
  return get<Comment[]>(`${BACKEND_URL}/cards/${card.name}/comments`);
};

export const createComment = (card: Card, comment: CommentCreate) => {
  comment.cardId = card.id;
  return post<CommentCreate, Comment>(`${BACKEND_URL}/cards/${card.name}/comments`, comment);
};
