import { create } from 'zustand';

interface AppState {
  deviceToken: string | null;
  setDeviceToken: (token: string) => void;
  
  // App Settings Cache
  settings: any | null;
  setSettings: (settings: any) => void;

  // Loading States
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  deviceToken: null,
  setDeviceToken: (token) => set({ deviceToken: token }),
  
  settings: null,
  setSettings: (settings) => set({ settings }),
  
  isLoading: false,
  setIsLoading: (isLoading) => set({ isLoading }),
}));
