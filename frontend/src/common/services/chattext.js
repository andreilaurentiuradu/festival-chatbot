import axios from 'axios';
import { API_URL } from '../constants';

const instance = axios.create({
  baseURL: API_URL,
});

export function chatRequest(data) {
  return instance.post('chat', data);
}
