import axios from 'axios';

console.log('API URL:', import.meta.env.VITE_API_URL);

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

export const uploadImages = (files) => {
  const formData = new FormData();
  files.forEach(file => formData.append('images', file));
  console.log('Sended formData', formData);
  console.log(API.baseURL);
  const response = API.post('/jobs/', formData);
  return response;
};

export const getJobStatus = (jobId) => API.get(`/jobs/${jobId}/status`);
export const getReport = (jobId) => API.get(`/jobs/${jobId}/report`);