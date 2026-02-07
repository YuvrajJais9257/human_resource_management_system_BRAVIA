// src/api/api.js
import axios from "axios";

const API = axios.create({
  // Use the env variable, or fallback to a local default
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export default API;