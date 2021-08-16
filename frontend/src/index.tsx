import React from 'react';
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import './index.scss';
import './scss/material-dashboard.scss';
import App from './App';
import { SENTRY_DSN } from './config';

Sentry.init({
  dsn: SENTRY_DSN,
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0,
});

ReactDOM.render(
  <Router>
    <App />
  </Router>,
  document.getElementById('root')
);
