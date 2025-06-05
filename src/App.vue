<template>
  <div class="app-container">
    <div class="chat-container">
      <div class="header">
        <div class="title">
          <span class="logo-emoji">🦊</span>
          <h1>AI代码助手</h1>
        </div>
        <div class="header-actions">
          <button class="history-btn" @click="showHistory = true">
            历史记录
          </button>
          <button class="history-btn" @click="showTasks = true">
            任务管理
          </button>
          <ModelSelector
            :models="availableModels"
            v-model="selectedModel"
          />
        </div>
      </div>
      <ChatWindow 
        :messages="messages"
        :loading="loading"
      />
      <div class="input-container">
        <textarea 
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="输入您的问题..."
        />
        <button 
          @click="sendMessage"
          :disabled="loading"
        >
          发送
        </button>
      </div>
    </div>
    <HistoryPanel
      :is-open="showHistory"
      @close="closeHistory"
    />
    <TaskPanel
      :is-open="showTasks"
      @close="closeTasks"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import ChatWindow from './components/ChatWindow.vue'
import ModelSelector from './components/ModelSelector.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import TaskPanel from './components/TaskPanel.vue'
import { sendChatMessage } from './services/api'

export default {
  components: {
    ChatWindow,
    ModelSelector,
    HistoryPanel,
    TaskPanel
  },
  setup() {
    const messages = ref([])
    const userInput = ref('')
    const loading = ref(false)
    const selectedModel = ref('hunyuan')
    const availableModels = ref([
      { id: 'hunyuan', name: '腾讯混元' },
      { id: 'qianwen', name: '通义千问' },
      { id: 'wenxin', name: '文心一言' }
    ])
    const showHistory = ref(false)
    const showTasks = ref(false)

    const sendMessage = async () => {
      if (!userInput.value.trim() || loading.value) return
      
      const userMessage = {
        role: 'user',
        content: userInput.value
      }
      
      messages.value.push(userMessage)
      loading.value = true
      userInput.value = ''

      try {
        const response = await sendChatMessage({
          message: userMessage.content,
          model: selectedModel.value
        })
        
        messages.value.push({
          role: 'assistant',
          content: response.message
        })
      } catch (error) {
        console.error('发送消息失败:', error)
        messages.value.push({
          role: 'system',
          content: '抱歉，发生了错误，请稍后重试。'
        })
      } finally {
        loading.value = false
      }
    }

    const closeHistory = () => {
      showHistory.value = false
    }

    const closeTasks = () => {
      showTasks.value = false
    }

    return {
      messages,
      userInput,
      loading,
      selectedModel,
      availableModels,
      sendMessage,
      showHistory,
      closeHistory,
      showTasks,
      closeTasks
    }
  }
}
</script> 

<style>
.logo-emoji {
  font-size: 32px;
  line-height: 1;
}

.title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.history-btn {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.history-btn:hover {
  opacity: 0.9;
}
</style> 