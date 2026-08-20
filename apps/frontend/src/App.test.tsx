import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { AppProviders } from './app/providers/AppProviders';

describe('App Foundation', () => {
  it('renders the application', () => {
    render(<AppProviders />);
    expect(screen.getByText(/Casino Platform Frontend/i)).toBeInTheDocument();
  });
});