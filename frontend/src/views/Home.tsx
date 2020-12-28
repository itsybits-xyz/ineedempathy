import React, { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';

const urls = [
  'wss://echo.websocket.org',
  'wss://demos.kaazing.com/echo',
];

interface message {
  data: string
}

export const Home = () => {
  //Public API that will echo messages sent to it back to the client
  const [socketUrl, setSocketUrl] = useState<string>(urls[0]);
  const [messageHistory, setMessageHistory] = useState<message[]>([]);

  const {
    sendMessage,
    lastMessage,
    readyState,
  } = useWebSocket(socketUrl);

  useEffect(
    () => {
      if (lastMessage) {
        setMessageHistory((prevHistory) => [...prevHistory, lastMessage]);
      }
    },
    [lastMessage],
  );

  const handleClickToggleSocketUrl = useCallback(() =>
    setSocketUrl((prevUrl) => prevUrl === urls[0] ? urls[1] : urls[0]), []);

  const handleClickSendMessage = useCallback(() =>
    sendMessage('Hello'), []);

  const connectionStatus = {
    [ReadyState.CONNECTING]: 'Connecting',
    [ReadyState.OPEN]: 'Open',
    [ReadyState.CLOSING]: 'Closing',
    [ReadyState.CLOSED]: 'Closed',
    [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
  }[readyState];

  return (
    <div>
      <p>
        <button
          onClick={handleClickToggleSocketUrl}
        >
          Click Me to toggle Socket URL
        </button>
        <button
          onClick={handleClickSendMessage}
          disabled={readyState !== ReadyState.OPEN}
        >
          Click Me to send 'Hello'
        </button>
      </p>
      <p>Socket URL: {socketUrl}</p>
      <p>The WebSocket is currently {connectionStatus}</p>
      {lastMessage && <p>Last message: {lastMessage.data}</p>}
      <ul>
        {messageHistory.map((message, idx) => <li key={idx}>{message.data}</li>)}
      </ul>
    </div>
  );
};
