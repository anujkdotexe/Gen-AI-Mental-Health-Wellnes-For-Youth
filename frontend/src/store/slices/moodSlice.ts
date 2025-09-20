import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

export interface MoodEntry {
  id: string;
  user_id: string;
  mood_level: number;
  notes: string | null;
  triggers: string | null;
  date: string;
}

export interface MoodState {
  entries: MoodEntry[];
  isLoading: boolean;
  error: string | null;
  selectedEntry: MoodEntry | null;
}

const initialState: MoodState = {
  entries: [],
  selectedEntry: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const createMoodEntry = createAsyncThunk(
  'mood/create',
  async (moodData: { mood_level: number; notes?: string; triggers?: string[]; activities?: string[] }, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch('http://localhost:8000/api/mood/entries', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.auth.token}`,
        },
        body: JSON.stringify(moodData),
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to create mood entry');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

export const getMoodEntries = createAsyncThunk(
  'mood/getEntries',
  async (_, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch('http://localhost:8000/api/mood/entries', {
        headers: {
          'Authorization': `Bearer ${state.auth.token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to get mood entries');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

export const getMoodInsights = createAsyncThunk(
  'mood/getInsights',
  async (days: number = 30, { rejectWithValue, getState }) => {
    try {
      const state = getState() as { auth: { token: string } };
      const response = await fetch(`http://localhost:8000/api/mood/insights?days=${days}`, {
        headers: {
          'Authorization': `Bearer ${state.auth.token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        return rejectWithValue(error.detail || 'Failed to get mood insights');
      }

      return await response.json();
    } catch (error: any) {
      return rejectWithValue(error.message || 'Network error');
    }
  }
);

const moodSlice = createSlice({
  name: 'mood',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setSelectedEntry: (state, action: PayloadAction<MoodEntry | null>) => {
      state.selectedEntry = action.payload;
    },
    clearSelectedEntry: (state) => {
      state.selectedEntry = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Create mood entry
      .addCase(createMoodEntry.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createMoodEntry.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries.unshift(action.payload);
        state.selectedEntry = action.payload;
        state.error = null;
      })
      .addCase(createMoodEntry.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get mood entries
      .addCase(getMoodEntries.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getMoodEntries.fulfilled, (state, action) => {
        state.isLoading = false;
        state.entries = Array.isArray(action.payload) ? action.payload : action.payload?.entries || [];
        state.error = null;
      })
      .addCase(getMoodEntries.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      // Get mood insights
      .addCase(getMoodInsights.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(getMoodInsights.fulfilled, (state, action) => {
        state.isLoading = false;
        state.error = null;
      })
      .addCase(getMoodInsights.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearError, setSelectedEntry, clearSelectedEntry } = moodSlice.actions;
export default moodSlice.reducer;