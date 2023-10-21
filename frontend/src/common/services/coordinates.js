import axios from 'axios';
import { API_URL } from '../constants';

const instance = axios.create({
  baseURL: API_URL,
});


export function coordinatesRequest(data) {
  return instance.post('coordinates', data);
}
