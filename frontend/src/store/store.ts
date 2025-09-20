import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import moodReducer from './slices/moodSlice';
import journalReducer from './slices/journalSlice';
import conversationReducer from './slices/conversationSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    mood: moodReducer,
    journal: journalReducer,
    conversation: conversationReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Export typed hooks for use throughout the app
export const useAppDispatch = () => store.dispatch;
export const useAppSelector = (fn: (state: RootState) => any) => fn(store.getState());