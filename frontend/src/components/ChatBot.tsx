import React, { useState, useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../store/store';
import { 
  startConversation, 
  sendMessage, 
  fetchConversations, 
  selectActiveConversation,
  selectConversations,
  selectIsLoading,
  selectError 
} from '../store/slices/conversationSlice';
import { 
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  ExclamationTriangleIcon,
  HeartIcon,
  CpuChipIcon,
  UsersIcon,
  FaceSmileIcon,
  FaceFrownIcon
} from '@heroicons/react/24/outline';

interface Message {
  id: string;
  content: string;
  is_user: boolean;
  timestamp: string;
  sentiment_score?: number;
  emotions?: { [key: string]: number };
  crisis_detected?: boolean;
}

const ChatBot: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const activeConversation = useSelector((state: RootState) => selectActiveConversation(state));
  const conversations = useSelector((state: RootState) => selectConversations(state));
  const isLoading = useSelector((state: RootState) => selectIsLoading(state));
  const error = useSelector((state: RootState) => selectError(state));
  
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showCrisisResources, setShowCrisisResources] = useState(false);
  const [sentimentHistory, setSentimentHistory] = useState<number[]>([]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // Load conversations on mount
    dispatch(fetchConversations());
    
    // Start a new conversation if none exists
    if (conversations.length === 0) {
      dispatch(startConversation(null));
    }
  }, [dispatch, conversations.length]);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    scrollToBottom();
  }, [activeConversation?.messages]);

  useEffect(() => {
    // Focus input when component mounts
    inputRef.current?.focus();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!message.trim() || !activeConversation || isLoading) return;

    const messageText = message.trim();
    setMessage('');
    setIsTyping(true);

    try {
      const result = await dispatch(sendMessage({
        conversationId: activeConversation.id,
        content: messageText
      })).unwrap();

      // Track sentiment history
      if (result.analysis?.sentiment_score !== undefined) {
        setSentimentHistory(prev => [...prev.slice(-9), result.analysis.sentiment_score]);
      }

      // Show crisis resources if crisis detected
      if (result.analysis?.crisis_detected) {
        setShowCrisisResources(true);
      }

    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getSentimentIcon = (score?: number) => {
    if (!score) return <div className="w-4 h-4 rounded-full bg-gray-400"></div>;
    if (score > 0.1) return <FaceSmileIcon className="w-4 h-4 text-green-500" />;
    if (score < -0.1) return <FaceFrownIcon className="w-4 h-4 text-red-500" />;
    return <div className="w-4 h-4 rounded-full bg-yellow-500"></div>;
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getEmotionColor = (emotion: string, score: number) => {
    const colors: { [key: string]: string } = {
      happy: 'bg-yellow-100 text-yellow-800',
      sad: 'bg-blue-100 text-blue-800',
      angry: 'bg-red-100 text-red-800',
      anxious: 'bg-purple-100 text-purple-800',
      neutral: 'bg-gray-100 text-gray-800',
      fear: 'bg-indigo-100 text-indigo-800',
      surprise: 'bg-pink-100 text-pink-800'
    };
    return colors[emotion] || 'bg-gray-100 text-gray-800';
  };

  if (error) {
    return (
      <div className="flex items-center justify-center h-96 bg-red-50 rounded-lg">
        <div className="text-center">
          <ExclamationTriangleIcon className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-red-800 mb-2">Connection Error</h3>
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => dispatch(fetchConversations())}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto h-[600px] bg-white rounded-lg shadow-lg flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center space-x-3">
          <ChatBubbleLeftRightIcon className="w-6 h-6" />
          <div>
            <h2 className="text-lg font-semibold">MindSpark AI Companion</h2>
            <p className="text-purple-100 text-sm">Your supportive mental wellness assistant</p>
          </div>
        </div>
        
        {/* Sentiment Trend */}
        {sentimentHistory.length > 0 && (
          <div className="mt-3 flex items-center space-x-2">
            <span className="text-sm text-purple-100">Mood trend:</span>
            <div className="flex space-x-1">
              {sentimentHistory.slice(-5).map((score, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full ${
                    score > 0.1 ? 'bg-green-300' : 
                    score < -0.1 ? 'bg-red-300' : 'bg-yellow-300'
                  }`}
                />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Crisis Resources Banner */}
      {showCrisisResources && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <ExclamationTriangleIcon className="w-5 h-5 text-red-400 mt-0.5 mr-3" />
            <div className="flex-1">
              <h3 className="text-sm font-medium text-red-800">
                Support Resources Available
              </h3>
              <div className="mt-2 text-sm text-red-700">
                <p className="mb-2">If you're in crisis, please reach out:</p>
                <div className="space-y-1">
                  <p><strong>Emergency:</strong> 911</p>
                  <p><strong>Crisis Line:</strong> 988 (24/7)</p>
                  <p><strong>Text Support:</strong> Text HOME to 741741</p>
                </div>
              </div>
              <button
                onClick={() => setShowCrisisResources(false)}
                className="mt-2 text-xs text-red-600 hover:text-red-800 underline"
              >
                Hide resources
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {activeConversation?.messages?.map((msg: Message) => (
          <div
            key={msg.id}
            className={`flex ${msg.is_user ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                msg.is_user
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
              
              {/* Message metadata */}
              <div className={`mt-2 flex items-center justify-between text-xs ${
                msg.is_user ? 'text-blue-100' : 'text-gray-500'
              }`}>
                <span>{formatTime(msg.timestamp)}</span>
                {msg.is_user && msg.sentiment_score !== undefined && (
                  <div className="flex items-center space-x-1">
                    {getSentimentIcon(msg.sentiment_score)}
                  </div>
                )}
              </div>
              
              {/* Emotions display for user messages */}
              {msg.is_user && msg.emotions && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {Object.entries(msg.emotions)
                    .filter(([_, score]) => score > 0.3)
                    .slice(0, 3)
                    .map(([emotion, score]) => (
                      <span
                        key={emotion}
                        className={`text-xs px-2 py-1 rounded-full ${getEmotionColor(emotion, score)}`}
                      >
                        {emotion} ({Math.round(score * 100)}%)
                      </span>
                    ))
                  }
                </div>
              )}
              
              {/* Crisis warning for user messages */}
              {msg.crisis_detected && msg.is_user && (
                <div className="mt-2 flex items-center space-x-1 text-red-200">
                  <ExclamationTriangleIcon className="w-3 h-3" />
                  <span className="text-xs">Support resources available</span>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Typing indicator */}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share what's on your mind..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!message.trim() || isLoading}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg transition-colors flex items-center space-x-2"
          >
            <PaperAirplaneIcon className="w-4 h-4" />
          </button>
        </div>
        
        {/* Quick actions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            onClick={() => setMessage("I'm feeling anxious today")}
            className="text-xs bg-purple-100 text-purple-700 px-3 py-1 rounded-full hover:bg-purple-200 transition-colors"
          >
            I'm feeling anxious
          </button>
          <button
            onClick={() => setMessage("I need some coping strategies")}
            className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full hover:bg-blue-200 transition-colors"
          >
            Need coping strategies
          </button>
          <button
            onClick={() => setMessage("Can you help me process my emotions?")}
            className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full hover:bg-green-200 transition-colors"
          >
            Process emotions
          </button>
        </div>
      </div>

      {/* Footer with features */}
      <div className="bg-gray-50 px-4 py-2 rounded-b-lg border-t">
        <div className="flex items-center justify-center space-x-6 text-xs text-gray-500">
          <div className="flex items-center space-x-1">
            <HeartIcon className="w-3 h-3" />
            <span>Empathetic AI</span>
          </div>
          <div className="flex items-center space-x-1">
            <CpuChipIcon className="w-3 h-3" />
            <span>Evidence-based</span>
          </div>
          <div className="flex items-center space-x-1">
            <UsersIcon className="w-3 h-3" />
            <span>Crisis support</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;