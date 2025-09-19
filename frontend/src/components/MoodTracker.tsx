import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { createMoodEntry, getMoodEntries } from '../store/slices/moodSlice';
import { HeartIcon } from '@heroicons/react/24/outline';
import type { RootState } from '../store/store';

const MoodTracker: React.FC = () => {
  const dispatch = useAppDispatch();
  const { entries, isLoading, error } = useAppSelector((state: RootState) => state.mood);
  const [selectedMood, setSelectedMood] = useState<number | null>(null);
  const [notes, setNotes] = useState('');
  const [triggers, setTriggers] = useState<string[]>([]);
  const [activities, setActivities] = useState<string[]>([]);

  useEffect(() => {
    dispatch(getMoodEntries());
  }, [dispatch]);

  const moodOptions = [
    { level: 1, label: 'Very Low', color: 'bg-red-500', emoji: '😢' },
    { level: 2, label: 'Low', color: 'bg-red-400', emoji: '😞' },
    { level: 3, label: 'Poor', color: 'bg-orange-400', emoji: '😕' },
    { level: 4, label: 'Fair', color: 'bg-yellow-400', emoji: '😐' },
    { level: 5, label: 'Okay', color: 'bg-yellow-300', emoji: '🙂' },
    { level: 6, label: 'Good', color: 'bg-green-300', emoji: '😊' },
    { level: 7, label: 'Very Good', color: 'bg-green-400', emoji: '😄' },
    { level: 8, label: 'Great', color: 'bg-green-500', emoji: '😆' },
    { level: 9, label: 'Excellent', color: 'bg-blue-400', emoji: '🤩' },
    { level: 10, label: 'Amazing', color: 'bg-purple-500', emoji: '🥳' },
  ];

  const commonTriggers = [
    'Work/School', 'Relationships', 'Money', 'Health', 'Family', 
    'Social Media', 'Weather', 'Sleep', 'Exercise', 'News'
  ];

  const commonActivities = [
    'Exercise', 'Reading', 'Music', 'TV/Movies', 'Socializing',
    'Cooking', 'Gaming', 'Art', 'Nature', 'Meditation'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedMood === null) return;

    try {
      await dispatch(createMoodEntry({
        mood_level: selectedMood,
        notes: notes || undefined,
        triggers: triggers.length > 0 ? triggers : undefined,
        activities: activities.length > 0 ? activities : undefined,
      })).unwrap();

      // Reset form
      setSelectedMood(null);
      setNotes('');
      setTriggers([]);
      setActivities([]);
    } catch (error) {
      // Error handled by Redux
    }
  };

  const toggleTrigger = (trigger: string) => {
    setTriggers(prev => 
      prev.includes(trigger) 
        ? prev.filter(t => t !== trigger)
        : [...prev, trigger]
    );
  };

  const toggleActivity = (activity: string) => {
    setActivities(prev => 
      prev.includes(activity) 
        ? prev.filter(a => a !== activity)
        : [...prev, activity]
    );
  };

  const todaysEntry = entries.find(entry => {
    const today = new Date().toDateString();
    const entryDate = new Date(entry.date).toDateString();
    return today === entryDate;
  });

  if (todaysEntry) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-3xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="text-center">
                <div className="mx-auto h-20 w-20 rounded-full bg-green-100 flex items-center justify-center">
                  <HeartIcon className="h-10 w-10 text-green-600" />
                </div>
                <h1 className="mt-4 text-2xl font-bold text-gray-900">
                  Mood Already Tracked Today!
                </h1>
                <p className="mt-2 text-gray-600">
                  You've already recorded your mood today. Your mood level was {todaysEntry.mood_level}/10.
                </p>
                <div className="mt-6">
                  <span className="text-4xl">
                    {moodOptions.find(m => m.level === todaysEntry.mood_level)?.emoji}
                  </span>
                  <p className="text-lg font-medium text-gray-900 mt-2">
                    {moodOptions.find(m => m.level === todaysEntry.mood_level)?.label}
                  </p>
                </div>
                {todaysEntry.notes && (
                  <div className="mt-4 bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600">{todaysEntry.notes}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Track Your Mood</h1>
          <p className="mt-2 text-gray-600">
            How are you feeling today? Take a moment to reflect on your current emotional state.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Mood Selection */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Rate your overall mood (1-10)
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
              {moodOptions.map((mood) => (
                <button
                  key={mood.level}
                  type="button"
                  onClick={() => setSelectedMood(mood.level)}
                  className={`relative rounded-lg p-4 text-center transition-all ${
                    selectedMood === mood.level
                      ? `${mood.color} text-white shadow-lg scale-105`
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  <div className="text-2xl mb-1">{mood.emoji}</div>
                  <div className="text-xs font-medium">{mood.level}</div>
                  <div className="text-xs">{mood.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Triggers */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              What influenced your mood? (Optional)
            </h2>
            <div className="flex flex-wrap gap-2">
              {commonTriggers.map((trigger) => (
                <button
                  key={trigger}
                  type="button"
                  onClick={() => toggleTrigger(trigger)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    triggers.includes(trigger)
                      ? 'bg-indigo-100 text-indigo-800 border-2 border-indigo-300'
                      : 'bg-gray-100 text-gray-700 border-2 border-transparent hover:bg-gray-200'
                  }`}
                >
                  {trigger}
                </button>
              ))}
            </div>
          </div>

          {/* Activities */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              What activities did you do today? (Optional)
            </h2>
            <div className="flex flex-wrap gap-2">
              {commonActivities.map((activity) => (
                <button
                  key={activity}
                  type="button"
                  onClick={() => toggleActivity(activity)}
                  className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                    activities.includes(activity)
                      ? 'bg-green-100 text-green-800 border-2 border-green-300'
                      : 'bg-gray-100 text-gray-700 border-2 border-transparent hover:bg-gray-200'
                  }`}
                >
                  {activity}
                </button>
              ))}
            </div>
          </div>

          {/* Notes */}
          <div className="bg-white shadow rounded-lg p-6">
            <label htmlFor="notes" className="block text-lg font-medium text-gray-900 mb-4">
              Additional notes (Optional)
            </label>
            <textarea
              id="notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="How are you feeling? What's on your mind today?"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="text-sm text-red-800">{error}</div>
            </div>
          )}

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={selectedMood === null || isLoading}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Saving...' : 'Track Mood'}
            </button>
          </div>
        </form>

        {/* Recent Entries */}
        {entries.length > 0 && (
          <div className="mt-8 bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Mood History</h2>
            <div className="space-y-3">
              {entries.slice(0, 7).map((entry) => {
                const mood = moodOptions.find(m => m.level === entry.mood_level);
                return (
                  <div key={entry.id} className="flex items-center justify-between py-2 border-b last:border-b-0">
                    <div className="flex items-center space-x-3">
                      <span className="text-xl">{mood?.emoji}</span>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {mood?.label} ({entry.mood_level}/10)
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(entry.date).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    {entry.notes && (
                      <div className="text-xs text-gray-600 max-w-xs truncate">
                        {entry.notes}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MoodTracker;