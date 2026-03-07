<template>
  <div class="app-shell">
    <aside class="panel panel-left">
      <div class="brand">
        <div class="brand-logo">⚡</div>
        <div>
          <h1>Cursor Cloud Agent</h1>
          <p>云端智能开发助手</p>
        </div>
      </div>

      <div class="section">
        <div class="section-title">快捷任务</div>
        <button
          v-for="action in quickActions"
          :key="action.title"
          class="quick-action"
          @click="applyQuickAction(action.prompt)"
        >
          <span class="quick-action-title">{{ action.title }}</span>
          <span class="quick-action-desc">{{ action.description }}</span>
        </button>
      </div>

      <div class="section">
        <div class="section-title">最近会话</div>
        <div v-if="historyLoading" class="muted-text">正在加载会话...</div>
        <div v-else-if="recentConversations.length === 0" class="muted-text">
          暂无历史会话
        </div>
        <button
          v-for="conversation in recentConversations"
          :key="conversation.id"
          class="conversation-chip"
          @click="loadConversation(conversation)"
        >
          <span>{{ conversation.model_name || '未知模型' }}</span>
          <small>{{ formatTime(conversation.created_at) }}</small>
        </button>
      </div>
    </aside>

    <main class="panel panel-main">
      <header class="main-header">
        <div class="header-title">
          <h2>Agent 控制台</h2>
          <span class="status-dot">
            <span class="dot" />
            在线
          </span>
        </div>

        <div class="header-actions">
          <ModelSelector :models="availableModels" v-model="selectedModel" />
          <button class="secondary-btn" @click="showHistory = true">历史记录</button>
          <button class="secondary-btn" @click="startNewSession">新会话</button>
        </div>
      </header>

      <ChatWindow :messages="messages" :loading="loading" />

      <div class="composer">
        <textarea
          ref="inputRef"
          v-model="userInput"
          class="composer-input"
          placeholder="描述你希望 Agent 完成的任务，例如：分析这段日志并定位根因"
          @keydown="handleComposerKeydown"
        />
        <div class="composer-foot">
          <span class="muted-text">Enter 发送，Shift + Enter 换行</span>
          <button class="primary-btn" :disabled="loading || !userInput.trim()" @click="sendMessage">
            {{ loading ? '处理中...' : '发送任务' }}
          </button>
        </div>
      </div>
    </main>

    <aside class="panel panel-right">
      <div class="section-title">运行状态</div>
      <div class="runtime-card">
        <div class="runtime-row">
          <span>当前模型</span>
          <strong>{{ activeModelName }}</strong>
        </div>
        <div class="runtime-row">
          <span>消息总数</span>
          <strong>{{ messages.length }}</strong>
        </div>
        <div class="runtime-row">
          <span>执行状态</span>
          <strong>{{ loading ? '运行中' : '空闲' }}</strong>
        </div>
      </div>

      <div class="section-title">最近事件</div>
      <div class="event-list">
        <div v-for="event in runtimeEvents" :key="event.id" class="event-item">
          <span class="event-icon">{{ event.icon }}</span>
          <div>
            <p>{{ event.text }}</p>
            <small>{{ event.time }}</small>
          </div>
        </div>
      </div>
    </aside>

    <HistoryPanel
      :is-open="showHistory"
      @close="showHistory = false"
      @select-conversation="loadConversation"
    />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import ChatWindow from './components/ChatWindow.vue'
import ModelSelector from './components/ModelSelector.vue'
import HistoryPanel from './components/HistoryPanel.vue'
import { getConversations, sendChatMessage } from './services/api'

const inputRef = ref(null)
const showHistory = ref(false)
const loading = ref(false)
const historyLoading = ref(false)
const userInput = ref('')
const messages = ref([
  {
    role: 'assistant',
    content:
      '你好，我是 Cursor Cloud Agent。你可以让我执行代码实现、问题排查、测试编写或重构建议。'
  }
])

const selectedModel = ref('claude-3-7-sonnet')
const availableModels = ref([
  { id: 'claude-3-7-sonnet', name: 'Claude 3.7 Sonnet' },
  { id: 'gpt-4.1', name: 'GPT-4.1' },
  { id: 'gemini-2.0-flash', name: 'Gemini 2.0 Flash' }
])

const recentConversations = ref([])

const quickActions = [
  {
    title: '代码审查',
    description: '扫描风险与潜在回归',
    prompt: '请对当前改动做一次严格代码审查，并按严重级别输出问题。'
  },
  {
    title: '生成测试',
    description: '补全关键测试用例',
    prompt: '请为当前模块生成单元测试，覆盖正常流程、边界情况和异常路径。'
  },
  {
    title: '排查构建失败',
    description: '分析并修复 CI 报错',
    prompt: '请根据报错日志定位构建失败根因，并给出可执行修复方案。'
  }
]

const activeModelName = computed(() => {
  const model = availableModels.value.find((item) => item.id === selectedModel.value)
  return model ? model.name : selectedModel.value
})

const runtimeEvents = computed(() => {
  const latest = messages.value.slice(-6)
  return latest.map((message, index) => {
    const iconMap = {
      user: '👤',
      assistant: '🤖',
      system: '⚠️'
    }
    return {
      id: `${index}-${message.role}-${message.content.length}`,
      icon: iconMap[message.role] || '🧩',
      text: message.content.slice(0, 42) + (message.content.length > 42 ? '...' : ''),
      time: new Date().toLocaleTimeString()
    }
  })
})

const formatTime = (timestamp) => {
  if (!timestamp) return '--'
  return new Date(timestamp).toLocaleString()
}

const fetchRecentConversations = async () => {
  historyLoading.value = true
  try {
    const data = await getConversations()
    recentConversations.value = Array.isArray(data) ? data.slice(0, 8) : []
  } catch (error) {
    console.error('加载最近会话失败:', error)
    recentConversations.value = []
  } finally {
    historyLoading.value = false
  }
}

const startNewSession = () => {
  messages.value = [
    {
      role: 'assistant',
      content: '已创建新会话。告诉我你希望在仓库中完成什么任务。'
    }
  ]
  userInput.value = ''
  inputRef.value?.focus()
}

const applyQuickAction = (prompt) => {
  userInput.value = prompt
  inputRef.value?.focus()
}

const loadConversation = (conversation) => {
  if (!conversation) return
  const nextMessages = []

  if (conversation.user_message) {
    nextMessages.push({
      role: 'user',
      content: conversation.user_message
    })
  }

  if (conversation.assistant_message) {
    nextMessages.push({
      role: 'assistant',
      content: conversation.assistant_message
    })
  }

  messages.value =
    nextMessages.length > 0
      ? nextMessages
      : [
          {
            role: 'system',
            content: '该历史会话内容为空或格式不完整。'
          }
        ]
  showHistory.value = false
}

const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content || loading.value) return

  messages.value.push({
    role: 'user',
    content
  })
  userInput.value = ''
  loading.value = true

  try {
    const response = await sendChatMessage({
      message: content,
      model: selectedModel.value
    })

    messages.value.push({
      role: 'assistant',
      content: response?.message || '任务已执行完成，但未返回内容。'
    })
    fetchRecentConversations()
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({
      role: 'system',
      content: '请求失败：当前无法连接到 Agent 服务，请稍后重试。'
    })
  } finally {
    loading.value = false
  }
}

const handleComposerKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

fetchRecentConversations()
</script>