export interface EnvConfig {
  BACKEND_URL: string;
  SOCKET_URL: string;
}
export interface EnvConfigs {
  [key: string]: EnvConfig;
}
const configFor = (envString: string):EnvConfig => {
  const confs:EnvConfigs = {
    production: {
      BACKEND_URL: 'http://ineedempathy.com/api',
      SOCKET_URL: 'ws://ineedempathy.com/api',
    },
    development: {
      BACKEND_URL: 'http://127.0.0.1:8000/api',
      SOCKET_URL: 'ws://127.0.0.1:8000/api',
    },
  };
  return confs[envString] || {
    BACKEND_URL: 'http://127.0.0.1:8000/api',
    SOCKET_URL: 'ws://127.0.0.1:8000/api',
  };
}

export const BACKEND_URL = configFor(process.env.NODE_ENV).BACKEND_URL;
export const SOCKET_URL = configFor(process.env.NODE_ENV).SOCKET_URL;
