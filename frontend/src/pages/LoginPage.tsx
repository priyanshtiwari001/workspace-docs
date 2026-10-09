// src/pages/LoginPage.tsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import { AuthLayout } from '../components/AuthLayout';
import { Button, Input } from '../components/ui';

export const LoginPage = () => {
  const navigate = useNavigate();
  
  // TODO: Add your local state for form data
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // TODO: Add state for loading and error handling (e.g., from TanStack Query mutation)
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    // TODO: Implement your login API call here
    // try {
    //   await login({ email, password });
    //   navigate('/workspaces'); // Redirect on success
    // } catch (err) {
    //   setError("Invalid email or password."); // Map this from your uniform error format
    // } finally {
    //   setIsSubmitting(false);
    // }
    
    console.log('Logging in with:', { email, password });
    setIsSubmitting(false);
  };

  return (
    <AuthLayout
      title="Log in to your account"
      subtitle="Enter your credentials to access your workspaces"
      footer={
        <>
          Don't have an account?{' '}
          <Link to="/auth/register" className="font-medium text-zinc-900 hover:underline">
            Sign up
          </Link>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Global Error State UI */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 text-sm rounded-md p-3">
            {error}
          </div>
        )}

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-zinc-700 mb-1">
            Email
          </label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="w-full"
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-1">
            <label htmlFor="password" className="block text-sm font-medium text-zinc-700">
              Password
            </label>
            {/* Optional: Forgot password link UI rule */}
            <button type="button" className="text-xs text-zinc-500 hover:text-zinc-700">
              Forgot password?
            </button>
          </div>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full"
          />
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Logging in...' : 'Log in'}
        </Button>
      </form>
    </AuthLayout>
  );
};