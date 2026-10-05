// src/components/Layout.tsx
import React from 'react';
import { Link, Outlet } from 'react-router';



export const Layout = () => {
  return (
    <div className="h-screen flex flex-col bg-slate-100 text-slate-800">
      {/* Top Bar */}
      <header className="h-14 border-b border-slate-200 bg-slate-900 text-slate-100 shadow-sm">
        <div className="mx-auto flex h-full w-full items-center justify-between px-4">
          {/* Workspace Switcher */}
          <div className="flex items-center gap-2">
            <select
              className="rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1.5 text-sm font-medium text-slate-100 shadow-sm outline-none transition focus:border-indigo-400 focus:ring-2 focus:ring-indigo-500/20"
              // TODO: Map over workspaces, handle onChange to switch workspace
            >
              <option className="bg-slate-800 text-slate-100">My Workspace</option>
            </select>
          </div>

          {/* User Menu */}
          <div className="relative">
            <button className="flex items-center gap-2 rounded-md px-2.5 py-1.5 text-sm font-medium text-slate-100 transition hover:bg-slate-800">
              <div className="h-7 w-7 rounded-full border border-slate-600 bg-gradient-to-br from-slate-200 to-slate-400" />
              <span>User Name</span>
            </button>
            {/* TODO: Add dropdown for Logout, Settings */}
          </div>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-60 border-r border-slate-200 bg-white/90 p-4 shadow-sm backdrop-blur-sm">
          <nav className="flex flex-col gap-1 text-sm">
            <Link
              to="/"
              className="rounded-lg px-3 py-2 font-medium text-slate-900 transition hover:bg-slate-100 hover:text-slate-900"
            >
              Workspace
            </Link>
            <Link
              to="/members"
              className="rounded-lg px-3 py-2 text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
            >
              Members
            </Link>
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto bg-slate-100">
          <Outlet />
        </main>
      </div>
    </div>
  );
};