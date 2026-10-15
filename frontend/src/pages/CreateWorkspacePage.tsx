import React from 'react';
import { Link } from 'react-router';
import { Button, Input, Card } from '../components/ui';

export const CreateWorkspacePage: React.FC = () => {
  // Pure UI - No frontend logic added
  // TODO: Add state and form handling logic here

  return (
    <div className="p-8 max-w-xl mx-auto space-y-6">
      <div>
        <Link to="/" className="text-sm text-zinc-500 hover:underline">
          &larr; Back to Workspaces
        </Link>
        <h1 className="text-2xl font-bold mt-2">Create Workspace</h1>
        <p className="text-sm text-zinc-500">
          Set up a new workspace for your notes and team.
        </p>
      </div>

      <Card className="p-6 space-y-4 bg-white">
        <div>
          <label 
            htmlFor="page-workspace-name" 
            className="block text-sm font-medium text-zinc-700 mb-1"
          >
            Workspace Name
          </label>
          <Input
            id="page-workspace-name"
            type="text"
            placeholder="e.g. My Workspace"
            // TODO: Bind value and onChange here
          />
        </div>

        <div className="flex justify-end gap-2 pt-2">
          <Link to="/">
            <Button variant="outline">Cancel</Button>
          </Link>
          <Button>
            {/* TODO: Add onClick handler for creating workspace */}
            Create Workspace
          </Button>
        </div>
      </Card>
    </div>
  );
};
