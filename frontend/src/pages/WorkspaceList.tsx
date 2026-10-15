import React, { useState } from 'react';
import { Button, Card } from '../components/ui';
import { CreateWorkspaceModal } from '../components/CreateWorkspaceModal';

export const WorkspaceList: React.FC = () => {
  // UI-only modal visibility toggle
  const [isModalOpen, setIsModalOpen] = useState(false);

  // TODO: Fetch workspaces using TanStack Query (GET /workspaces)
  const workspaces: any[] = []; // Replace with query data

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Your Workspaces</h1>
        {/* On click of Create Workspace / + New Workspace, opens the component taking name as input */}
        <Button onClick={() => setIsModalOpen(true)}>+ New Workspace</Button>
      </div>

      {/* TODO: Handle Empty state cleanly */}
      {workspaces.length === 0 ? (
        <Card className="p-12 flex flex-col items-center justify-center border-dashed">
          <p className="text-zinc-500 mb-4">You don't have any workspaces yet.</p>
          <Button onClick={() => setIsModalOpen(true)}>Create your first workspace</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* TODO: Map through workspaces */}
          {/* {workspaces.map(ws => (
            <Card key={ws.id} className="p-4 hover:shadow-md transition-shadow cursor-pointer">
              <h3 className="font-semibold">{ws.name}</h3>
              <p className="text-sm text-zinc-500">Created at: {ws.createdAt}</p>
            </Card>
          ))} */}
        </div>
      )}

      {/* Component taking name as input on click of Create Workspace */}
      <CreateWorkspaceModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};