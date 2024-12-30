import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

export const api = axios.create({
  baseURL: API_BASE_URL,
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
    return response.data
  } catch (error) {
    console.error('API Error:', error)
    throw error
  }
} 