import { Component, type ReactNode } from 'react';
import { ErrorState } from '../ui/ErrorState';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorState
          title="Критическая ошибка"
          message={this.state.error?.message || 'Приложение столкнулось с неожиданной ошибкой'}
          onRetry={() => window.location.reload()}
        />
      );
    }

    return this.props.children;
  }
}