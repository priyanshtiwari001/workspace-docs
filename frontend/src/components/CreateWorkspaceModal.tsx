import React, { useState, useEffect } from 'react';
import { X, Building2 } from 'lucide-react';
import { Button, Input } from './ui';

export interface CreateWorkspaceModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateWorkspaceModal: React.FC<CreateWorkspaceModalProps> = ({
  isOpen,
  onClose,
}) => {
  // UI Form States - Ready for interview implementation
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Close on Escape key (UX polish, doesn't interfere with interview logic)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Reset form state when modal closes/opens
  useEffect(() => {
    if (isOpen) {
      setName('');
      setError(null);
      setIsLoading(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // ========================================================
    // TODO [Interview Task: Core Creation Logic]
    // --------------------------------------------------------
    // 1. Validation:
    //    if (!name.trim()) {
    //      setError("Workspace name is required.");
    //      return;
    //    }
    //
    // 2. Trigger API Call / Mutation:
    //    try {
    //      setIsLoading(true);
    //      setError(null);
    //      await createWorkspaceApi({ name }); // POST /workspaces
    //
    // 3. Cache Invalidation & Cleanup:
    //      queryClient.invalidateQueries({ queryKey: ['workspaces'] });
    //      onClose();
    //    } catch (err: any) {
    //      setError(err?.message || "Failed to create workspace");
    //    } finally {
    //      setIsLoading(false);
    //    }
    // ========================================================
    console.log('Submitting workspace name:', name);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity" 
        onClick={onClose} 
      />

      {/* Modal Card */}
      <div 
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="relative w-full max-w-md rounded-2xl border border-slate-200 bg-white p-6 shadow-2xl z-10 space-y-5 animate-in fade-in zoom-in-95 duration-150"
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Building2 className="w-4 h-4" />
            </div>
            <div>
              <h2 id="modal-title" className="text-base font-bold text-slate-900">
                Create Workspace
              </h2>
              <p className="text-xs text-slate-500">
                Create a space to organize your notes and collaborate.
              </p>
            </div>
          </div>

          <button 
            type="button" 
            onClick={onClose} 
            className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-100 transition-colors"
            aria-label="Close"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Error Message Display UI */}
          {error && (
            <div className="p-3 text-xs font-medium text-rose-700 bg-rose-50 border border-rose-200 rounded-lg">
              {error}
            </div>
          )}

          {/* Workspace Name Input */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label 
                htmlFor="workspace-name-input" 
                className="text-xs font-semibold text-slate-700"
              >
                Workspace Name <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-slate-400 font-mono">
                {name.length}/50
              </span>
            </div>

            <Input
              id="workspace-name-input"
              type="text"
              autoFocus
              maxLength={50}
              placeholder="e.g. Engineering Docs, Acme Corp"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                if (error) setError(null);
              }}
              disabled={isLoading}
              className="text-sm border-slate-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 rounded-xl"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100">
            <Button 
              type="button" 
              variant="outline" 
              onClick={onClose}
              disabled={isLoading}
              className="px-4 text-xs font-medium text-slate-700 border-slate-300"
            >
              Cancel
            </Button>
            <Button 
              type="submit"
              disabled={isLoading}
              className="px-4 text-xs font-semibold bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm"
            >
              {isLoading ? 'Creating...' : 'Create Workspace'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
