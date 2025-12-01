import axios from 'axios';

const timeApiClient = axios.create({
  baseURL: 'https://timeapi.io/',
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  timeout: 8000,
});

export const timeApi = {
  getAvailableTimezones: () => timeApiClient.get<string[]>('api/timezone/availabletimezones'),
  getTimezoneInfo: (timeZone: string) =>
    timeApiClient.get('api/timezone/zone', {
      params: { timeZone },
    }),
};

export default timeApi;
