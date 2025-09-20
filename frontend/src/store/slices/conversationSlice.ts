import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export interface Message {
  id: string;
  conversation_id: string;
  content: string;
  is_user: boolean;
  timestamp: string;
  sentiment_score?: number;
  emotions?: { [key: string]: number };
  crisis_detected?: boolean;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string | null;
  created_at: string;
  messages?: Message[];
}

export interface ConversationState {
  conversations: Conversation[];
  activeConversation: Conversation | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: ConversationState = {
  conversations: [],
  activeConversation: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchConversations = createAsyncThunk(
  'conversation/fetchConversations',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { auth: { token: string | null } };
      const token = state.auth.token;

      if (!token) {
        return rejectWithValue('No token available');
      }

      const response = await fetch('http://localhost:8000/api/conversation/list', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        return rejectWithValue('Failed to fetch conversations');
      }

      const data = await response.json();
      return data.conversations || [];
    } catch (error) {
      return rejectWithValue('Network error');
    }
  }
);

export const createConversation = createAsyncThunk(
  'conversation/create',
  async (title: string | null, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { auth: { token: string | null } };
      const token = state.auth.token;

      if (!token) {
        return rejectWithValue('No token available');
      }

      const response = await fetch('http://localhost:8000/api/conversation/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ title }),
      });

      if (!response.ok) {
        return rejectWithValue('Failed to create conversation');
      }

      return await response.json();
    } catch (error) {
      return rejectWithValue('Network error');
    }
  }
);

export const fetchConversationDetails = createAsyncThunk(
  'conversation/fetchConversationDetails',
  async (conversationId: string, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { auth: { token: string | null } };
      const token = state.auth.token;

      if (!token) {
        return rejectWithValue('No token available');
      }

      const response = await fetch(`http://localhost:8000/api/conversation/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        return rejectWithValue('Failed to fetch conversation details');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      return rejectWithValue('Network error');
    }
  }
);

export const sendMessage = createAsyncThunk(
  'conversation/sendMessage',
  async ({ conversationId, content }: { conversationId: string; content: string }, { getState, rejectWithValue }) => {
    try {
      const state = getState() as { auth: { token: string | null } };
      const token = state.auth.token;

      if (!token) {
        return rejectWithValue('No token available');
      }

      const response = await fetch(`http://localhost:8000/api/conversation/${conversationId}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) {
        return rejectWithValue('Failed to send message');
      }

      const result = await response.json();
      // Backend returns both user_message and ai_message
      return {
        user_message: result.user_message,
        ai_message: result.ai_message,
        analysis: result.analysis
      };
    } catch (error) {
      return rejectWithValue('Network error');
    }
  }
);

const conversationSlice = createSlice({
  name: 'conversation',
  initialState,
  reducers: {
    setActiveConversation: (state, action: PayloadAction<Conversation | null>) => {
      state.activeConversation = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    clearConversations: (state) => {
      state.conversations = [];
      state.activeConversation = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch conversations
      .addCase(fetchConversations.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchConversations.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations = Array.isArray(action.payload) ? action.payload : action.payload?.conversations || [];
        state.error = null;
      })
      .addCase(fetchConversations.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Create conversation
      .addCase(createConversation.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createConversation.fulfilled, (state, action) => {
        state.isLoading = false;
        state.conversations.unshift(action.payload);
        state.activeConversation = action.payload;
        state.error = null;
      })
      .addCase(createConversation.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Fetch conversation details
      .addCase(fetchConversationDetails.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchConversationDetails.fulfilled, (state, action) => {
        state.isLoading = false;
        // Set the fetched conversation as active
        state.activeConversation = action.payload;
        // Update the conversation in the list if it exists
        const existingIndex = state.conversations.findIndex(conv => conv.id === action.payload.id);
        if (existingIndex !== -1) {
          state.conversations[existingIndex] = action.payload;
        }
        state.error = null;
      })
      .addCase(fetchConversationDetails.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Send message
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        if (state.activeConversation && action.payload) {
          if (!state.activeConversation.messages) {
            state.activeConversation.messages = [];
          }
          // Add both user message and AI response
          const payload = action.payload as any;
          if (payload.user_message) {
            state.activeConversation.messages.push(payload.user_message);
          }
          if (payload.ai_message) {
            state.activeConversation.messages.push(payload.ai_message);
          }
        }
        state.error = null;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setActiveConversation, clearError, clearConversations } = conversationSlice.actions;

// Selectors
export const selectConversations = (state: { conversation: ConversationState }) => state.conversation.conversations;
export const selectActiveConversation = (state: { conversation: ConversationState }) => state.conversation.activeConversation;
export const selectIsLoading = (state: { conversation: ConversationState }) => state.conversation.isLoading;
export const selectError = (state: { conversation: ConversationState }) => state.conversation.error;

// Alias for createConversation to match the ChatBot component
export const startConversation = createConversation;

export default conversationSlice.reducer;
