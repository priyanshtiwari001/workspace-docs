// src/pages/AuthPage.tsx
import React, { useState } from 'react';
import { Button, Input, Card } from "../components/ui"

export const AuthPage = () => {
  const [mode, setMode] = useState<'login' | 'register'>('login');

  // TODO: Add local state for email, password, name
  // TODO: Add onSubmit handler to call your API and navigate

  return (
    <div className="h-screen flex items-center justify-center bg-zinc-50">
      <Card className="w-full max-w-md p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">
          {mode === 'login' ? 'Log In' : 'Create an Account'}
        </h1>
        
        <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); /* TODO: Handle submit */ }}>
          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <Input type="text" placeholder="John Doe" required />
            </div>
          )}
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <Input type="email" placeholder="you@example.com" required />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <Input type="password" placeholder="********" required />
          </div>
          
          {/* TODO: Render validation errors from your uniform error format here */}
          {/* <p className="text-red-500 text-sm">{error}</p> */}

          <Button type="submit" className="w-full">
            {mode === 'login' ? 'Log In' : 'Sign Up'}
          </Button>
        </form>

        <div className="mt-4 text-center text-sm text-zinc-600">
          {mode === 'login' ? (
            <p>Don't have an account? <button onClick={() => setMode('register')} className="text-blue-600 font-medium">Sign up</button></p>
          ) : (
            <p>Already have an account? <button onClick={() => setMode('login')} className="text-blue-600 font-medium">Log in</button></p>
          )}
        </div>
      </Card>
    </div>
  );
};