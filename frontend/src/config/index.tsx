export interface EnvConfig {
  BACKEND_URL: string;
  SOCKET_URL: string;
  SENTRY_DSN: string;
}
export interface EnvConfigs {
  [key: string]: EnvConfig;
}
const configFor = (envString: string):EnvConfig => {
  const confs:EnvConfigs = {
    production: {
      BACKEND_URL: 'http://ineedempathy.com/api',
      SOCKET_URL: 'ws://ineedempathy.com/api',
      SENTRY_DSN: 'https://3355964559bb41f9a7d44b99c3f7123b@o948279.ingest.sentry.io/5897485',
    },
    development: {
      BACKEND_URL: 'http://127.0.0.1:8000/api',
      SOCKET_URL: 'ws://127.0.0.1:8000/api',
      SENTRY_DSN: '',
    },
  };
  return confs[envString] || {
    BACKEND_URL: 'http://127.0.0.1:8000/api',
    SOCKET_URL: 'ws://127.0.0.1:8000/api',
    SENTRY_DSN: '',
  };
}

export const BACKEND_URL = configFor(process.env.NODE_ENV).BACKEND_URL;
export const SOCKET_URL = configFor(process.env.NODE_ENV).SOCKET_URL;
export const SENTRY_DSN = configFor(process.env.NODE_ENV).SENTRY_DSN;
