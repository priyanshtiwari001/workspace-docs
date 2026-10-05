// src/pages/NoteEditor.tsx
import React, { useState } from 'react';
import { Button, Input, Textarea } from '../components/ui';

interface NoteEditorProps {
  // TODO: Pass role down from parent or use a custom hook (e.g., useRole())
  role: 'owner' | 'editor' | 'viewer';
}

export const NoteEditor = ({ role }: NoteEditorProps) => {
  // TODO: Fetch note by ID (GET /notes/{id})
  // TODO: Setup TanStack Query mutation for saving (PUT /notes/{id})
  
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  // UI rule: Hide/disable actions user's role can't perform
  const isReadOnly = role === 'viewer';

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        {/* TODO: Add a back button to return to notes list */}
        <Button variant="ghost" onClick={() => {}}>&larr; Back to Notes</Button>
        
        {!isReadOnly && (
          <Button 
            // TODO: Add onClick to trigger mutation
            // TODO: Disable if no changes made
          >
            Save Note
          </Button>
        )}
      </div>

      <div className="space-y-6 bg-white border rounded-lg p-8">
        <Input 
          type="text"
          placeholder="Untitled Note"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isReadOnly}
          className="text-2xl font-bold border-none focus:ring-0 px-0"
        />
        
        <Textarea 
          placeholder="Start writing your note here..." 
          value={content}
          onChange={(e) => setContent(e.target.value)}
          disabled={isReadOnly}
          className="min-h-[400px] border-none focus:ring-0 px-0 resize-none"
        />
      </div>

      {isReadOnly && (
        <p className="text-center text-sm text-zinc-500 mt-4">
          You are a viewer in this workspace. You cannot edit notes.
        </p>
      )}
    </div>
  );
};