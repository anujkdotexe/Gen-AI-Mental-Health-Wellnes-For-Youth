import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { createJournalEntry, getJournalEntries, updateJournalEntry, type JournalEntry } from '../store/slices/journalSlice';
import type { RootState } from '../store/store';

const Journal: React.FC = () => {
  const dispatch = useAppDispatch();
  const { entries, isLoading, error } = useAppSelector((state: RootState) => state.journal);
  const { isAuthenticated, user } = useAppSelector((state: RootState) => state.auth);
  const [showNewEntry, setShowNewEntry] = useState(false);
  const [editingEntry, setEditingEntry] = useState<JournalEntry | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    mood: '',
  });

  useEffect(() => {
    dispatch(getJournalEntries());
  }, [dispatch]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const entryData = {
      title: formData.title || undefined,
      content: formData.content,
      mood: formData.mood || undefined,
    };

    if (editingEntry) {
      await dispatch(updateJournalEntry({ id: editingEntry.id, ...entryData }));
      setEditingEntry(null);
    } else {
      await dispatch(createJournalEntry(entryData));
      setShowNewEntry(false);
    }

    setFormData({ title: '', content: '', mood: '' });
  };

  const handleEdit = (entry: JournalEntry) => {
    setEditingEntry(entry);
    setFormData({
      title: entry.title || '',
      content: entry.content,
      mood: entry.mood || '',
    });
    setShowNewEntry(true);
  };

  const filteredEntries = entries.filter((entry: JournalEntry) => {
    const matchesSearch = (entry.title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                         entry.content.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  // Check if user needs to login to access journaling
  const needsLogin = !isAuthenticated || user?.is_anonymous;

  if (needsLogin) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center space-x-3">
            <h1 className="text-3xl font-bold text-gray-900">📖 Journal</h1>
            <span className="text-sm text-green-600 font-medium">(Free to use)</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Login Required for Journaling
          </h2>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Please log in to access your personal journal. Your entries are private, secure, and completely free to use.
          </p>
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-green-700 font-medium">✨ Journaling is completely free!</p>
              <p className="text-green-600 text-sm mt-1">
                Create an account to start tracking your thoughts, moods, and personal growth.
              </p>
            </div>
            <button
              onClick={() => window.location.href = '/auth'}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors font-medium"
            >
              Login to Start Journaling
            </button>
          </div>
          <div className="mt-6 text-sm text-gray-500">
            <p>🔐 Your journal entries are private and encrypted</p>
            <p>📊 Track your mood patterns over time</p>
            <p>🧠 AI-powered insights to support your mental wellness</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center space-x-3">
          <h1 className="text-3xl font-bold text-gray-900">📖 Journal</h1>
          <span className="text-sm text-green-600 font-medium">(Free to use)</span>
        </div>
        <button
          onClick={() => setShowNewEntry(true)}
          className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center space-x-2"
        >
          <span>+ New Entry</span>
        </button>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <input
          type="text"
          placeholder="Search entries..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        />
      </div>

      {/* New/Edit Entry Form */}
      {showNewEntry && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {editingEntry ? 'Edit Entry' : 'New Journal Entry'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Title (Optional)</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="What's on your mind?"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Content</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                required
                rows={6}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Write your thoughts here..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Mood (Optional)</label>
              <input
                type="text"
                value={formData.mood}
                onChange={(e) => setFormData({ ...formData, mood: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="How are you feeling? (e.g., happy, sad, anxious)"
              />
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                disabled={isLoading}
                className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
              >
                {isLoading ? 'Saving...' : (editingEntry ? 'Update Entry' : 'Save Entry')}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowNewEntry(false);
                  setEditingEntry(null);
                  setFormData({ title: '', content: '', mood: '' });
                }}
                className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Entries List */}
      <div className="space-y-6">
        {isLoading && entries.length === 0 ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
            <p className="text-gray-600 mt-2">Loading journal entries...</p>
          </div>
        ) : filteredEntries.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-600 mb-2">📖 No Journal Entries</h3>
            <p className="text-gray-500 mb-4">
              {searchTerm ? 'No entries match your search criteria.' : 'Start writing your first journal entry!'}
            </p>
            {!searchTerm && (
              <button
                onClick={() => setShowNewEntry(true)}
                className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
              >
                Write First Entry
              </button>
            )}
          </div>
        ) : (
          filteredEntries.map((entry: JournalEntry) => (
            <div key={entry.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  {entry.title && (
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{entry.title}</h3>
                  )}
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <div className="flex items-center space-x-1">
                      <span>📅 {new Date(entry.created_at).toLocaleDateString()}</span>
                    </div>
                    {entry.mood && (
                      <div className="flex items-center space-x-1">
                        <span>Mood: {entry.mood}</span>
                      </div>
                    )}
                    {entry.is_ai_generated && (
                      <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full text-xs">
                        AI Generated
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => handleEdit(entry)}
                    className="p-2 text-gray-500 hover:text-purple-600 transition-colors"
                    title="Edit entry"
                  >
                    ✏️
                  </button>
                </div>
              </div>
              <p className="text-gray-700 whitespace-pre-wrap">{entry.content}</p>
              {entry.prompt && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-700">
                    <strong>Prompt:</strong> {entry.prompt}
                  </p>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Journal;