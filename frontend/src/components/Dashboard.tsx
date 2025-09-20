import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { getCurrentUser } from '../store/slices/authSlice';
import { getMoodEntries } from '../store/slices/moodSlice';
import { getJournalEntries } from '../store/slices/journalSlice';
import { fetchConversations } from '../store/slices/conversationSlice';
import type { RootState } from '../store/store';
import { 
  HeartIcon, 
  BookOpenIcon, 
  ChatBubbleLeftRightIcon,
  ExclamationTriangleIcon,
  CalendarDaysIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user, isLoading: authLoading } = useAppSelector((state: RootState) => state.auth);
  const { entries: moodEntries = [], isLoading: moodLoading } = useAppSelector((state: RootState) => state.mood);
  const { entries: journalEntries = [], isLoading: journalLoading } = useAppSelector((state: RootState) => state.journal);
  const { conversations = [], isLoading: conversationLoading } = useAppSelector((state: RootState) => state.conversation);

  useEffect(() => {
    if (user && !user.is_anonymous) {
      // Only load data for registered users, not anonymous users
      dispatch(getCurrentUser());
      dispatch(getMoodEntries());
      dispatch(getJournalEntries());
      dispatch(fetchConversations());
    }
  }, [dispatch, user]);

  // Show loading only if we're still authenticating
  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const todaysMood = moodEntries.find(entry => {
    const today = new Date().toDateString();
    const entryDate = new Date(entry.date).toDateString();
    return today === entryDate;
  });

  const recentJournalEntries = journalEntries.slice(0, 3);
  const activeConversations = conversations.slice(0, 3);

  const quickActions = [
    {
      title: 'Track Mood',
      description: 'How are you feeling today?',
      href: '/mood',
      icon: HeartIcon,
      color: 'bg-pink-500',
      disabled: !!todaysMood,
    },
    {
      title: 'Write in Journal',
      description: 'Express your thoughts and feelings',
      href: '/journal',
      icon: BookOpenIcon,
      color: 'bg-blue-500',
      disabled: false,
    },
    {
      title: 'Talk to AI',
      description: 'Get support anytime you need it',
      href: '/chat',
      icon: ChatBubbleLeftRightIcon,
      color: 'bg-green-500',
      disabled: false,
    },
    {
      title: 'Crisis Support',
      description: 'Immediate help when you need it most',
      href: '/crisis',
      icon: ExclamationTriangleIcon,
      color: 'bg-red-500',
      disabled: false,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Welcome Section */}
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="flex items-center">
                <div className="flex-1">
                  <h1 className="text-2xl font-bold text-gray-900">
                    Welcome back{user?.username ? `, ${user.username}` : ''}!
                  </h1>
                  <p className="mt-2 text-sm text-gray-600">
                    {user?.is_anonymous
                      ? "You're using MindSpark AI anonymously. Your privacy is fully protected."
                      : "Here's how you're doing on your mental wellness journey."
                    }
                  </p>
                </div>
                <div className="flex-shrink-0">
                  <div className="h-16 w-16 rounded-full bg-indigo-100 flex items-center justify-center">
                    <span className="text-2xl font-bold text-indigo-600">
                      {user?.is_anonymous ? '🎭' : '🌟'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <Link
                  key={action.title}
                  to={action.href}
                  className={`relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-md transition-shadow ${
                    action.disabled ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                  onClick={action.disabled ? (e) => e.preventDefault() : undefined}
                >
                  <div>
                    <span className={`rounded-lg inline-flex p-3 ${action.color} text-white`}>
                      <Icon className="h-6 w-6" aria-hidden="true" />
                    </span>
                  </div>
                  <div className="mt-8">
                    <h3 className="text-lg font-medium">
                      {action.title}
                      {action.disabled && (
                        <span className="ml-2 text-sm text-green-600">✓ Done today</span>
                      )}
                    </h3>
                    <p className="mt-2 text-sm text-gray-500">
                      {action.description}
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Today's Overview */}
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            {/* Today's Mood */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <HeartIcon className="h-6 w-6 text-pink-500" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Today's Mood</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {todaysMood ? (
                          <div className="flex items-center">
                            <span className="mr-2">{todaysMood.mood_level}/5</span>
                            <div className="flex-1 bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-pink-500 h-2 rounded-full" 
                                style={{ width: `${(todaysMood.mood_level / 5) * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        ) : (
                          <Link to="/mood" className="text-indigo-600 hover:text-indigo-500">
                            Track your mood
                          </Link>
                        )}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            {/* Journal Entries */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <BookOpenIcon className="h-6 w-6 text-blue-500" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Journal Entries</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {journalEntries.length} total
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            {/* AI Conversations */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ChatBubbleLeftRightIcon className="h-6 w-6 text-green-500" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">AI Conversations</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {conversations.length} conversations
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="px-4 py-6 sm:px-0">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h2>
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {recentJournalEntries.length === 0 && activeConversations.length === 0 ? (
                <li className="px-6 py-4">
                  <div className="text-center">
                    <CalendarDaysIcon className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No recent activity</h3>
                    <p className="mt-1 text-sm text-gray-500">
                      Start your mental wellness journey by tracking your mood or writing in your journal.
                    </p>
                  </div>
                </li>
              ) : (
                <>
                  {recentJournalEntries.map((entry) => (
                    <li key={`journal-${entry.id}`}>
                      <Link to={`/journal/${entry.id}`} className="block hover:bg-gray-50">
                        <div className="px-4 py-4 sm:px-6">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <BookOpenIcon className="h-5 w-5 text-blue-500 mr-3" />
                              <p className="text-sm font-medium text-indigo-600 truncate">
                                {entry.title || 'Journal Entry'}
                              </p>
                            </div>
                            <div className="ml-2 flex-shrink-0 flex">
                              <ClockIcon className="h-4 w-4 text-gray-400 mr-1" />
                              <p className="text-sm text-gray-500">
                                {new Date(entry.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="mt-2 sm:flex sm:justify-between">
                            <div className="sm:flex">
                              <p className="text-sm text-gray-500 truncate">
                                {entry.content.substring(0, 100)}...
                              </p>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </li>
                  ))}
                  {activeConversations.map((conversation) => (
                    <li key={`conversation-${conversation.id}`}>
                      <Link to={`/chat/${conversation.id}`} className="block hover:bg-gray-50">
                        <div className="px-4 py-4 sm:px-6">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <ChatBubbleLeftRightIcon className="h-5 w-5 text-green-500 mr-3" />
                              <p className="text-sm font-medium text-indigo-600 truncate">
                                {conversation.title || 'AI Conversation'}
                              </p>
                            </div>
                            <div className="ml-2 flex-shrink-0 flex">
                              <ClockIcon className="h-4 w-4 text-gray-400 mr-1" />
                              <p className="text-sm text-gray-500">
                                                                {new Date(conversation.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="mt-2 sm:flex sm:justify-between">
                            <div className="sm:flex">
                              <p className="text-sm text-gray-500">
                                {conversation.messages?.length || 0} messages
                              </p>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </li>
                  ))}
                </>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;