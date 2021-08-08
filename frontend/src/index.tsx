import React from 'react';
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import './index.scss';
import './scss/material-dashboard.scss';
import App from './App';

Sentry.init({
  dsn: "https://3355964559bb41f9a7d44b99c3f7123b@o948279.ingest.sentry.io/5897485",
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0,
});

ReactDOM.render(
  <Router>
    <App />
  </Router>,
  document.getElementById('root')
);
