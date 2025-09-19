import React, { useState } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { logout } from '../store/slices/authSlice';
import type { RootState } from '../store/store';

const PrivacySettings: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state: RootState) => state.auth);
  const [settings, setSettings] = useState({
    dataCollection: true,
    analytics: false,
    aiTraining: false,
    notifications: true,
    shareAnonymous: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSettingChange = (key: keyof typeof settings, value: boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSaveSettings = async () => {
    setIsLoading(true);
    setMessage(null);
    
    try {
      // Simulate API call to save privacy settings
      await new Promise(resolve => setTimeout(resolve, 1000));
      setMessage({ type: 'success', text: 'Privacy settings saved successfully!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to save settings. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteData = async () => {
    if (!window.confirm('Are you sure you want to delete all your data? This action cannot be undone.')) {
      return;
    }

    if (!window.confirm('This will permanently delete all your journal entries, mood data, and conversations. Are you absolutely sure?')) {
      return;
    }

    setIsLoading(true);
    try {
      // API call would go here to delete user data
      await new Promise(resolve => setTimeout(resolve, 2000));
      setMessage({ type: 'success', text: 'All data has been deleted. You will be logged out.' });
      setTimeout(() => {
        dispatch(logout());
      }, 2000);
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to delete data. Please contact support.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadData = async () => {
    setIsLoading(true);
    try {
      // Simulate data export
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Create a sample data export
      const exportData = {
        user: user,
        exportDate: new Date().toISOString(),
        journalEntries: '(Your journal entries would be included here)',
        moodData: '(Your mood tracking data would be included here)',
        conversations: '(Your AI conversations would be included here)',
        settings: settings,
      };
      
      const dataStr = JSON.stringify(exportData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `mindspark-data-export-${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      setMessage({ type: 'success', text: 'Data export completed successfully!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Failed to export data. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">🔒 Privacy & Settings</h1>
        <p className="text-gray-600">
          Manage your privacy preferences and data settings. Your privacy is our top priority.
        </p>
      </div>

      {message && (
        <div className={`border px-4 py-3 rounded-lg mb-6 ${
          message.type === 'success' 
            ? 'bg-green-50 border-green-200 text-green-700'
            : 'bg-red-50 border-red-200 text-red-700'
        }`}>
          {message.text}
        </div>
      )}

      {/* Account Information */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">👤 Account Information</h2>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Account Type:</span>
            <span className="font-medium">
              {user?.is_anonymous ? '🕶️ Anonymous User' : '👤 Registered User'}
            </span>
          </div>
          {user?.username && !user.is_anonymous && (
            <div className="flex justify-between">
              <span className="text-gray-600">User ID:</span>
              <span className="font-medium">{user.id}</span>
            </div>
          )}
          {user?.username && (
            <div className="flex justify-between">
              <span className="text-gray-600">Username:</span>
              <span className="font-medium">{user.username}</span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-gray-600">Member Since:</span>
            <span className="font-medium">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'Unknown'}
            </span>
          </div>
        </div>
      </div>

      {/* Privacy Settings */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">🛡️ Privacy Settings</h2>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Essential Data Collection</h3>
              <p className="text-sm text-gray-600">
                Required for app functionality (mood entries, journal entries)
              </p>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.dataCollection}
                onChange={(e) => handleSettingChange('dataCollection', e.target.checked)}
                className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Anonymous Analytics</h3>
              <p className="text-sm text-gray-600">
                Help improve the app with anonymous usage analytics
              </p>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.analytics}
                onChange={(e) => handleSettingChange('analytics', e.target.checked)}
                className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">AI Training Data</h3>
              <p className="text-sm text-gray-600">
                Allow anonymized conversations to improve AI responses (optional)
              </p>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.aiTraining}
                onChange={(e) => handleSettingChange('aiTraining', e.target.checked)}
                className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Push Notifications</h3>
              <p className="text-sm text-gray-600">
                Receive reminders for mood tracking and journal prompts
              </p>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.notifications}
                onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
            </div>
          </div>

          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Anonymous Research</h3>
              <p className="text-sm text-gray-600">
                Share anonymized data for mental health research (completely anonymous)
              </p>
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={settings.shareAnonymous}
                onChange={(e) => handleSettingChange('shareAnonymous', e.target.checked)}
                className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
              />
            </div>
          </div>
        </div>

        <div className="mt-6">
          <button
            onClick={handleSaveSettings}
            disabled={isLoading}
            className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
          >
            {isLoading ? 'Saving...' : 'Save Privacy Settings'}
          </button>
        </div>
      </div>

      {/* Data Management */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">📊 Data Management</h2>
        <div className="space-y-4">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-medium text-blue-900 mb-2">📥 Export Your Data</h3>
            <p className="text-sm text-blue-700 mb-3">
              Download a copy of all your data including journal entries, mood data, and settings.
            </p>
            <button
              onClick={handleDownloadData}
              disabled={isLoading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Preparing Export...' : 'Download My Data'}
            </button>
          </div>

          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <h3 className="font-medium text-red-900 mb-2">🗑️ Delete All Data</h3>
            <p className="text-sm text-red-700 mb-3">
              Permanently delete all your data from our servers. This action cannot be undone.
            </p>
            <button
              onClick={handleDeleteData}
              disabled={isLoading}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Deleting...' : 'Delete All My Data'}
            </button>
          </div>
        </div>
      </div>

      {/* Privacy Information */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-purple-900 mb-4">🔐 Our Privacy Commitment</h2>
        <div className="space-y-3 text-purple-700">
          <div className="flex items-start space-x-2">
            <span className="text-green-600 mt-1">✅</span>
            <p className="text-sm">All data is encrypted in transit and at rest</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 mt-1">✅</span>
            <p className="text-sm">We never sell or share your personal data</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 mt-1">✅</span>
            <p className="text-sm">Anonymous usage only requires minimal data</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 mt-1">✅</span>
            <p className="text-sm">You can delete your data at any time</p>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-green-600 mt-1">✅</span>
            <p className="text-sm">Open source code available for transparency</p>
          </div>
        </div>
        <div className="mt-4 p-3 bg-purple-100 rounded-lg">
          <p className="text-sm text-purple-800">
            <strong>Note:</strong> If you're using the anonymous mode, no personal information 
            is collected. Your data is only identified by a random ID that cannot be traced back to you.
          </p>
        </div>
      </div>
    </div>
  );
};

export default PrivacySettings;