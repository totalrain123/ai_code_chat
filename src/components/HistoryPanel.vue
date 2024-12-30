<template>
  <div class="history-panel" :class="{ 'is-open': isOpen }">
    <div class="history-header">
      <h2>历史记录</h2>
      <button 
        class="close-btn" 
        @click="handleClose"
        title="关闭"
      >×</button>
    </div>
    <div class="history-content">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="conversations.length === 0" class="empty">
        暂无历史记录
      </div>
      <div v-else class="conversation-list">
        <div v-for="conv in conversations" :key="conv.id" class="conversation-item">
          <div class="conversation-time">{{ formatTime(conv.created_at) }}</div>
          <div class="conversation-model">{{ conv.model_name }}</div>
          <div class="message user-message">
            <span class="avatar">👤</span>
            <div class="content">{{ conv.user_message }}</div>
          </div>
          <div class="message assistant-message">
            <span class="avatar">🦊</span>
            <div class="content">{{ conv.assistant_message }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { getConversations } from '../services/api'

export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['close'],
  
  setup(props, { emit }) {
    const conversations = ref([])
    const loading = ref(false)
    
    const handleClose = () => {
      emit('close')
    }
    
    const loadConversations = async () => {
      loading.value = true
      try {
        conversations.value = await getConversations()
      } catch (error) {
        console.error('加载历史记录失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleString()
    }
    
    onMounted(() => {
      loadConversations()
    })
    
    return {
      conversations,
      loading,
      formatTime,
      handleClose
    }
  }
}
</script>

<style scoped>
.history-panel {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: white;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 1000;
}

.history-panel.is-open {
  right: 0;
}

.history-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  color: #666;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f3f4f6;
  color: #1f2937;
}

.history-content {
  height: calc(100vh - 60px);
  overflow-y: auto;
  padding: 1rem;
}

.conversation-item {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.conversation-time {
  color: #666;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.conversation-model {
  color: var(--primary-color);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.message {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.avatar {
  font-size: 1.25rem;
}

.content {
  background: var(--bg-color);
  padding: 0.5rem;
  border-radius: 4px;
  flex: 1;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style> 