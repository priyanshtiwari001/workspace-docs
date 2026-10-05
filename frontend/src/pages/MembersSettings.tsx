// src/pages/MembersSettings.tsx
import React, { useState } from 'react';
import { Button, Input } from '../components/ui';

interface Member {
  id: string;
  email: string;
  role: 'owner' | 'editor' | 'viewer';
}

export const MembersSettings = () => {
  // TODO: Fetch members (GET /workspaces/{id}/members)
  // TODO: Get current user role to determine if they can manage members
  
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteRole, setInviteRole] = useState<'editor' | 'viewer'>('viewer');
  
  // Mock data for UI structure
  const members: Member[] = [
    { id: '1', email: 'alice@x.com', role: 'owner' },
    // { id: '2', email: 'bob@x.com', role: 'editor' },
  ];

  const currentUserRole: 'owner' | 'editor' | 'viewer' = 'owner'; // TODO: Replace with real logic
  const canManage = currentUserRole === 'owner';

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Members</h1>

      {/* Add Member Section - Hidden for Viewers/Editors */}
      {canManage && (
        <div className="mb-8 p-4 border rounded-lg bg-white">
          <h2 className="font-semibold mb-3">Invite Member</h2>
          <div className="flex gap-2">
            <Input 
              type="email" 
              placeholder="member@email.com" 
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              className="flex-1"
            />
            <select 
              className="border rounded-md px-3 bg-white text-sm"
              value={inviteRole}
              onChange={(e) => setInviteRole(e.target.value as 'editor' | 'viewer')}
            >
              <option value="viewer">Viewer</option>
              <option value="editor">Editor</option>
            </select>
            <Button 
              // TODO: Add POST /members logic
            >
              Add Member
            </Button>
          </div>
          {/* TODO: Show validation errors here */}
        </div>
      )}

      {/* Members List */}
      <div className="border rounded-lg bg-white overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-zinc-50 border-b">
            <tr>
              <th className="text-left p-4 font-medium">Email</th>
              <th className="text-left p-4 font-medium">Role</th>
              <th className="text-right p-4 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {/* TODO: Map members array here */}
            {members.map((member) => (
              <tr key={member.id} className="hover:bg-zinc-50">
                <td className="p-4">{member.email} {member.role === 'owner' && <span className="text-zinc-500 text-xs">(you)</span>}</td>
                <td className="p-4">
                  <select 
                    className="border rounded-md px-2 py-1 bg-transparent"
                    value={member.role}
                    disabled={!canManage || member.role === 'owner'}
                    // TODO: Add onChange to handle PATCH /members/{id}
                  >
                    <option value="owner">Owner</option>
                    <option value="editor">Editor</option>
                    <option value="viewer">Viewer</option>
                  </select>
                </td>
                <td className="p-4 text-right">
                  {canManage && member.role !== 'owner' && (
                    <Button 
                      variant="destructive" 
                      // TODO: Add DELETE /members/{id} logic
                    >
                      Remove
                    </Button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};