import { BACKEND_URL } from '../config';
import { Card, Room, RoomCreate } from '../schemas';
import {PromiseFn} from 'react-async';

async function http<T>(path: string, authenticated: boolean = true, config: RequestInit): Promise<T> {
  const headers = new Headers(); headers.append('Content-Type', 'application/json');
  if (authenticated) {
    const token = localStorage.getItem('token');
    headers.append('Authorization', `Bearer ${token}`);
  }
  const request = new Request(path, {headers, ...config});
  const response = await fetch(request);
  if (authenticated && (response.status === 401 || response.status === 403)) {
    localStorage.removeItem('token');
    localStorage.removeItem('permissions');
    return Promise.reject("Unauthorized Access!");
  }
  if (!response.ok) {
    const resp_json = await response.json().catch(() => (response.statusText));
    throw new Error(resp_json.detail ?? resp_json);
  }
  return await response.json();
}

export async function get<T>(path: string, authenticated: boolean = true, config?: RequestInit): Promise<T> {
  const init = { method: 'get', ...config };
  return await http<T>(path, authenticated, init);
}

export async function post<T, U>(
  path: string,
  body: T,
  authenticated: boolean = true,
  config?: RequestInit
): Promise<U> {
  const init = { method: 'post', body: JSON.stringify(body), ...config };
  return await http<U>(path, authenticated, init);
}

export async function put<T, U>(
  path: string,
  body: T,
  authenticated: boolean = true,
  config?: RequestInit
): Promise<U> {
  const init = { method: 'put', body: JSON.stringify(body), ...config };
  return await http<U>(path, authenticated, init);
}

export const getMessage = async () => {
  const response = await fetch(BACKEND_URL);
  const data = await response.json();
  if (data.msg) {
    return data.msg;
  }
  return Promise.reject('Failed to get message from backend');
};

export const getCards = async () => {
  return get<Card[]>(`${BACKEND_URL}/cards`);
};

export const getRooms = async () => {
  return get<Room[]>(`${BACKEND_URL}/rooms`);
};

export const getRoom: PromiseFn<Room> = async ({roomId}) => {
  return get<Room>(`${BACKEND_URL}/rooms/${roomId}`);
};

export const postRoom = async (payload: RoomCreate) => {
  return post<RoomCreate, Room>(`${BACKEND_URL}/rooms`, payload);
};
