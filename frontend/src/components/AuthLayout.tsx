// src/components/AuthLayout.tsx
import React from 'react';

interface AuthLayoutProps {
  title: string;
  subtitle: string;
  children: React.ReactNode;
  footer: React.ReactNode;
}

export const AuthLayout = ({ title, subtitle, children, footer }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-zinc-50 px-4">
      <div className="w-full max-w-md">
        {/* Logo / App Name Placeholder */}
        <div className="flex justify-center mb-8">
          <div className="h-10 w-10 rounded-md bg-zinc-900 flex items-center justify-center text-white font-bold">
            W
          </div>
        </div>

        <div className="bg-white p-8 border border-zinc-200 rounded-lg shadow-sm">
          <div className="mb-6 text-center">
            <h1 className="text-2xl font-bold text-zinc-900">{title}</h1>
            <p className="text-sm text-zinc-500 mt-1">{subtitle}</p>
          </div>

          {children}
        </div>

        <div className="mt-6 text-center text-sm text-zinc-600">
          {footer}
        </div>
      </div>
    </div>
  );
};