import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL
});

export const uploadImages = (files) => {
  const formData = new FormData();
  files.forEach(file => formData.append('images', file));
  return API.post('/jobs/', formData);
};

export const getJobStatus = (jobId) => API.get(`/jobs/${jobId}/status`);
export const getReport = (jobId) => API.get(`/jobs/${jobId}/report`);