// src/pages/RegisterPage.tsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import { AuthLayout } from '../components/AuthLayout';
import { Button, Input } from '../components/ui';

export const RegisterPage = () => {
  const navigate = useNavigate();

  // TODO: Add your local state for form data
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  // TODO: Add state for loading and error handling
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    // TODO: Implement your register API call here
    // try {
    //   await register({ name, email, password });
    //   navigate('/workspaces'); // Redirect on success
    // } catch (err) {
    //   setError("Email already in use."); // Map this from your uniform error format
    // } finally {
    //   setIsSubmitting(false);
    // }

    console.log('Registering with:', { name, email, password });
    setIsSubmitting(false);
  };

  return (
    <AuthLayout
      title="Create an account"
      subtitle="Start managing your workspace notes today"
      footer={
        <>
          Already have an account?{' '}
          <Link to="/auth/login" className="font-medium text-zinc-900 hover:underline">
            Log in
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
          <label htmlFor="name" className="block text-sm font-medium text-zinc-700 mb-1">
            Full Name
          </label>
          <Input
            id="name"
            type="text"
            autoComplete="name"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="John Doe"
            className="w-full"
          />
        </div>

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
          <label htmlFor="password" className="block text-sm font-medium text-zinc-700 mb-1">
            Password
          </label>
          <Input
            id="password"
            type="password"
            autoComplete="new-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Create a secure password"
            className="w-full"
          />
          {/* Optional: Password requirement hints UI rule */}
          <p className="text-xs text-zinc-500 mt-1">
            Must be at least 8 characters long.
          </p>
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? 'Creating account...' : 'Sign up'}
        </Button>
      </form>
    </AuthLayout>
  );
};