import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export interface JournalEntry {
  id: string;
  user_id: string;
  title?: string;
  content: string;
  mood?: string;
  prompt?: string;
  is_ai_generated: boolean;
  created_at: string;
  updated_at: string;
}

interface JournalState {
  entries: JournalEntry[];
  currentEntry: JournalEntry | null;
  prompts: string[];
  isLoading: boolean;
  error: string | null;
}

const initialState: JournalState = {
  entries: [],
  currentEntry: null,
  prompts: [],
  isLoading: false,
  error: null,
};

// Async thunks
export const createJournalEntry = createAsyncThunk(
  'journal/create',
  async (entryData: { title?: string; content: string; mood?: string; prompt?: string }, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch('http://localhost:8000/api/journal/entries', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.auth.token}`,
        },
        body: JSON.stringify(entryData),
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to create journal entry');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

export const getJournalEntries = createAsyncThunk(
  'journal/getEntries',
  async (_, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch('http://localhost:8000/api/journal/', {
        headers: {
          'Authorization': `Bearer ${state.auth.token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to get journal entries');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

export const getJournalPrompts = createAsyncThunk(
  'journal/getPrompts',
  async (_, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch('http://localhost:8000/api/journal/prompts', {
        headers: {
          'Authorization': `Bearer ${state.auth.token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to get journal prompts');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

export const updateJournalEntry = createAsyncThunk(
  'journal/update',
  async ({ id, ...updateData }: { id: string; title?: string; content?: string; mood?: string }, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch(`http://localhost:8000/journal/entries/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.auth.token}`,
        },
        body: JSON.stringify(updateData),
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to update journal entry');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

const journalSlice = createSlice({
  name: 'journal',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentEntry: (state, action: PayloadAction<JournalEntry>) => {
      state.currentEntry = action.payload;
    },
    clearCurrentEntry: (state) => {
      state.currentEntry = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create journal entry
      .addCase(createJournalEntry.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createJournalEntry.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries.unshift(action.payload);
        state.currentEntry = action.payload;
        state.error = null;
      })
      .addCase(createJournalEntry.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get journal entries
      .addCase(getJournalEntries.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getJournalEntries.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries = Array.isArray(action.payload) ? action.payload : action.payload?.entries || [];
        state.error = null;
      })
      .addCase(getJournalEntries.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get journal prompts
      .addCase(getJournalPrompts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getJournalPrompts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.prompts = action.payload.prompts || [];
        state.error = null;
      })
      .addCase(getJournalPrompts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Update journal entry
      .addCase(updateJournalEntry.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateJournalEntry.fulfilled, (state, action) => {
        state.isLoading = false;
        const index = state.entries.findIndex(entry => entry.id === action.payload.id);
        if (index !== -1) {
          state.entries[index] = action.payload;
        }
        if (state.currentEntry?.id === action.payload.id) {
          state.currentEntry = action.payload;
        }
        state.error = null;
      })
      .addCase(updateJournalEntry.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setCurrentEntry, clearCurrentEntry } = journalSlice.actions;
export default journalSlice.reducer;