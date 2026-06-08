import axios from 'axios';
import { Platform } from 'react-native';

const LOCAL_IP = '192.168.1.100'; // Kendi yerel IP adresinle değiştir
const BASE_URL = __DEV__ 
  ? Platform.OS === 'android' 
    ? 'http://10.0.2.2:8000/api/' 
    : `http://${LOCAL_IP}:8000/api/`
  : 'https://api.porsukapp.com/api/';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export const fetchExamDates = async () => {
  const response = await api.get('exam-dates/');
  return response.data;
};

export const fetchLatestDailyQuestion = async () => {
  const response = await api.get('daily-question/latest/');
  return response.data;
};

export const fetchDiagnosticTests = async () => {
  const response = await api.get('diagnostic-tests/');
  return response.data;
};

export const fetchDiagnosticTestDetail = async (id: number) => {
  const response = await api.get(`diagnostic-tests/${id}/`);
  return response.data;
};

export const createLeadContact = async (data: any) => {
  const response = await api.post('leads/', data);
  return response.data;
};

export const fetchAnnouncements = async () => {
  const response = await api.get('announcements/');
  return response.data;
};

export const fetchAppSettings = async () => {
  const response = await api.get('settings/');
  return response.data;
};

export const fetchRandomQuote = async () => {
  const response = await api.get('quotes/random/');
  return response.data;
};

export const fetchFormulas = async (topic?: string) => {
  const url = topic ? `formulas/?topic=${topic}` : 'formulas/';
  const response = await api.get(url);
  return response.data;
};

export const registerDeviceToken = async (token: string, device_name: string, platform: string) => {
  const response = await api.post('device-tokens/', { token, device_name, platform });
  return response.data;
};

export default api;
