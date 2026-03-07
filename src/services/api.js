import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const sendChatMessage = async (payload) => {
  try {
    const response = await api.post('/chat', payload)
    return response.data
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
}

export const getConversations = async () => {
  try {
    const response = await api.get('/conversations')
    return Array.isArray(response.data) ? response.data : []
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
} 