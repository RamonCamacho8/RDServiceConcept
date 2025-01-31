import { render, screen } from '@testing-library/react';
import App from './App';

test('renders upload button', () => {
  render(<App />);
  const uploadElement = screen.getByText(/Upload Images/i);
  expect(uploadElement).toBeInTheDocument();
});