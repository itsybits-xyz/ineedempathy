import React, { FC, useState } from "react";
import { Button } from 'react-bootstrap';
import { BoardGame } from "./BoardGame";
import { useAsync } from 'react-async';
import { getCards } from '../utils/api';

export interface RoomProps {
  match: {
    params: {
      name: string
    }
  }
}

export const Room: FC<RoomProps> = (props: RoomProps) => {
  const roomname = props?.match?.params?.name;
  const { data } = useAsync(getCards);
  const [username, setUsername] = useState<string>(localStorage.getItem(roomname) || "");
  const [ready, _setReady] = useState<boolean>(false);

  const setReady = (value:boolean) => {
    localStorage.setItem(roomname, username);
    return _setReady(value);
  };

  if (!ready) {
    return (
      <>
        <div>
          Type in your username to join {roomname}
        </div>
        <div>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value) } />
        </div>
        <div>
          <Button onClick={() => setReady(true)}>Join Now</Button>
        </div>
      </>
    );
  }

  return <BoardGame cards={data} roomname={roomname} username={username} />
};
