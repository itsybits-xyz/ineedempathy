import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home', () => {
  render(<App />);
  const linkElement = screen.getByText('Create an Empathy Room');
  expect(linkElement).toBeTruthy();
});
