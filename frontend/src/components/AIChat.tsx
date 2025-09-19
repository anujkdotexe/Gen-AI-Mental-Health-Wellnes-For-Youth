import React, { useState, useEffect, useRef } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks/redux';
import { createConversation, sendMessage, fetchConversations, type Message, type Conversation } from '../store/slices/conversationSlice';
import type { RootState } from '../store/store';

const AIChat: React.FC = () => {
  const dispatch = useAppDispatch();
  const { conversations, activeConversation, isLoading, error } = useAppSelector((state: RootState) => state.conversation);
  const [inputMessage, setInputMessage] = useState('');
  const [currentMessages, setCurrentMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    dispatch(fetchConversations());
  }, [dispatch]);

  useEffect(() => {
    if (activeConversation?.messages) {
      setCurrentMessages(activeConversation.messages);
    }
  }, [activeConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [currentMessages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleStartNewConversation = async () => {
    const result = await dispatch(createConversation(null));
    if (result.meta.requestStatus === 'fulfilled') {
      setCurrentMessages([]);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || !activeConversation || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      conversation_id: activeConversation.id,
      content: inputMessage,
      role: 'user',
      created_at: new Date().toISOString(),
    };

    setCurrentMessages(prev => [...prev, userMessage]);
    setInputMessage('');

    try {
      const result = await dispatch(sendMessage({
        conversationId: activeConversation.id,
        content: inputMessage,
      }));

      if (result.meta.requestStatus === 'fulfilled') {
        const aiResponse = result.payload as Message;
        setCurrentMessages(prev => [...prev, aiResponse]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleSelectConversation = (conversation: Conversation) => {
    setCurrentMessages(conversation.messages || []);
  };

  return (
    <div className="max-w-6xl mx-auto p-6 h-screen flex">
      {/* Conversations Sidebar */}
      <div className="w-1/3 pr-4">
        <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">🤖 AI Conversations</h2>
              <button
                onClick={handleStartNewConversation}
                className="bg-purple-600 text-white px-3 py-1 rounded-lg hover:bg-purple-700 transition-colors text-sm"
              >
                + New Chat
              </button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto">
            {conversations.length === 0 ? (
              <div className="p-4 text-center text-gray-500">
                <p>No conversations yet.</p>
                <p className="text-sm mt-2">Start a new chat to begin!</p>
              </div>
            ) : (
              <div className="space-y-2 p-4">
                {conversations.map((conversation: Conversation) => (
                  <div
                    key={conversation.id}
                    onClick={() => handleSelectConversation(conversation)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      activeConversation?.id === conversation.id
                        ? 'bg-purple-100 border-2 border-purple-300'
                        : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                    }`}
                  >
                    <h3 className="font-medium text-gray-900 truncate">
                      {conversation.title || 'Untitled Conversation'}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {new Date(conversation.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="w-2/3 flex flex-col">
        <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
          {/* Chat Header */}
          <div className="p-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              {activeConversation ? 'AI Mental Health Assistant' : 'Select or Start a Conversation'}
            </h2>
            {activeConversation && (
              <p className="text-sm text-gray-500 mt-1">
                Your privacy-first AI companion for mental wellness support
              </p>
            )}
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {!activeConversation ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="text-6xl mb-4">🤖</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  Welcome to Your AI Mental Health Assistant
                </h3>
                <p className="text-gray-500 mb-6 max-w-md">
                  Start a conversation to receive personalized support, mindfulness guidance, 
                  and coping strategies. Your conversations are private and secure.
                </p>
                <button
                  onClick={handleStartNewConversation}
                  className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors"
                >
                  Start Your First Conversation
                </button>
              </div>
            ) : currentMessages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <div className="text-4xl mb-4">💬</div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  Ready to Chat!
                </h3>
                <p className="text-gray-500 mb-4">
                  Share what's on your mind. I'm here to listen and support you.
                </p>
                <div className="space-y-2 text-sm text-gray-600">
                  <p>You can ask me about:</p>
                  <ul className="list-disc list-inside space-y-1">
                    <li>Stress management techniques</li>
                    <li>Coping with anxiety or depression</li>
                    <li>Mindfulness and relaxation</li>
                    <li>Sleep and self-care tips</li>
                    <li>Building healthy habits</li>
                  </ul>
                </div>
              </div>
            ) : (
              <>
                {currentMessages.map((message, index) => (
                  <div
                    key={message.id || index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.role === 'user'
                          ? 'bg-purple-600 text-white'
                          : 'bg-gray-100 text-gray-800 border'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className={`text-xs mt-1 ${
                        message.role === 'user' ? 'text-purple-200' : 'text-gray-500'
                      }`}>
                        {new Date(message.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Input Area */}
          {activeConversation && (
            <div className="p-4 border-t border-gray-200">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded-lg mb-4 text-sm">
                  {error}
                </div>
              )}
              <form onSubmit={handleSendMessage} className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Share what's on your mind..."
                  disabled={isLoading}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={isLoading || !inputMessage.trim()}
                  className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? '...' : 'Send'}
                </button>
              </form>
              <p className="text-xs text-gray-500 mt-2 text-center">
                💚 Your conversations are private and encrypted. If you're in crisis, please contact emergency services.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIChat;