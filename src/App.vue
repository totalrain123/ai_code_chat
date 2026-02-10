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
          <ModelSelector 
            :models="availableModels"
            :disabled="loadingModels || availableModels.length === 0"
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
          :disabled="loading || loadingModels || !selectedModel"
        >
          {{ loadingModels ? '加载模型中...' : '发送' }}
        </button>
      </div>
    </div>
    <HistoryPanel 
      :is-open="showHistory"
      @close="closeHistory"
    />
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import ChatWindow from './components/ChatWindow.vue'
import ModelSelector from './components/ModelSelector.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import { getModelConfigs, sendChatMessage } from './services/api'

export default {
  components: {
    ChatWindow,
    ModelSelector,
    HistoryPanel
  },
  setup() {
    const messages = ref([])
    const userInput = ref('')
    const loading = ref(false)
    const loadingModels = ref(false)
    const selectedModel = ref('')
    const fallbackModels = [
      { id: 'hunyuan', name: '腾讯混元' },
      { id: 'qianwen', name: '通义千问' },
      { id: 'wenxin', name: '文心一言' }
    ]
    const availableModels = ref([...fallbackModels])
    const showHistory = ref(false)

    const appendSystemMessage = (content) => {
      messages.value.push({
        role: 'system',
        content
      })
    }

    const loadModels = async () => {
      loadingModels.value = true
      try {
        const modelConfig = await getModelConfigs()
        const configuredModels = modelConfig.models.filter((model) => model.configured)
        availableModels.value = configuredModels.map((model) => ({
          id: model.id,
          name: model.name
        }))

        if (availableModels.value.length === 0) {
          selectedModel.value = ''
          appendSystemMessage('未检测到可用模型，请先完成 API Key 配置。')
          return
        }

        const hasDefault = availableModels.value.some(
          (model) => model.id === modelConfig.default_model
        )
        selectedModel.value = hasDefault
          ? modelConfig.default_model
          : availableModels.value[0].id
      } catch (error) {
        console.error('加载模型配置失败:', error)
        availableModels.value = [...fallbackModels]
        selectedModel.value = fallbackModels[0].id
        appendSystemMessage('模型配置加载失败，已使用默认模型列表。')
      } finally {
        loadingModels.value = false
      }
    }

    const sendMessage = async () => {
      if (!userInput.value.trim() || loading.value || loadingModels.value) return
      if (!selectedModel.value) {
        appendSystemMessage('当前没有可用模型，请检查模型配置。')
        return
      }
      
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
        appendSystemMessage('抱歉，发生了错误，请稍后重试。')
      } finally {
        loading.value = false
      }
    }

    const closeHistory = () => {
      showHistory.value = false
    }

    onMounted(() => {
      loadModels()
    })

    return {
      messages,
      userInput,
      loading,
      loadingModels,
      selectedModel,
      availableModels,
      sendMessage,
      loadModels,
      showHistory,
      closeHistory
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