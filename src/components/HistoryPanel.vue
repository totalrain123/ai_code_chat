<template>
  <div class="history-mask" :class="{ 'is-open': isOpen }" @click="handleClose" />
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
          <button
            v-for="conv in conversations"
            :key="conv.id"
            class="conversation-item"
            @click="handleSelect(conv)"
          >
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
          </button>
        </div>
      </div>
  </div>
</template>

<script>
import { onUnmounted, ref, watch } from 'vue'
import { getConversations } from '../services/api'

export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['close', 'select-conversation'],
  
  setup(props, { emit }) {
    const conversations = ref([])
    const loading = ref(false)
    
    const handleClose = () => {
      emit('close')
    }

    const handleSelect = (conversation) => {
      emit('select-conversation', conversation)
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
    
    watch(
      () => props.isOpen,
      (open) => {
        if (open) {
          loadConversations()
        }
      },
      { immediate: true }
    )

    watch(() => props.isOpen, (open) => {
      if (open) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    })

    onUnmounted(() => {
      document.body.style.overflow = ''
    })

    return {
      conversations,
      loading,
      formatTime,
      handleClose,
      handleSelect
    }
  }
}
</script>

<style scoped>
.history-mask {
  position: fixed;
  inset: 0;
  background: rgba(2, 5, 10, 0.45);
  z-index: 990;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}

.history-mask.is-open {
  opacity: 1;
  pointer-events: auto;
}

.history-panel {
  position: fixed;
  top: 0;
  right: -430px;
  width: 400px;
  height: 100vh;
  background: #121d31;
  border-left: 1px solid var(--color-border);
  box-shadow: -8px 0 30px rgba(0, 0, 0, 0.45);
  transition: right 0.3s ease;
  z-index: 1001;
}

.history-panel.is-open {
  right: 0;
}

.history-header {
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-header h2 {
  margin: 0;
  font-size: 1.1rem;
}

.close-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  color: var(--color-text);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #1b2942;
}

.history-content {
  height: calc(100vh - 60px);
  overflow-y: auto;
  padding: 1rem;
}

.conversation-item {
  width: 100%;
  text-align: left;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: #18253c;
  color: var(--color-text);
  padding: 1rem;
  margin-bottom: 1rem;
  cursor: pointer;
}

.conversation-item:hover {
  border-color: #35507a;
}

.conversation-time {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.conversation-model {
  color: var(--color-primary);
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
  background: #121d31;
  padding: 0.5rem;
  border-radius: 4px;
  flex: 1;
  max-height: 140px;
  overflow-y: auto;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}
</style> 