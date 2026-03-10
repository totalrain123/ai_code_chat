<template>
  <div class="message-item" :class="messageClass">
    <div class="avatar">
      {{ message.role === 'user' ? '👤' : message.role === 'system' ? '⚠️' : '🤖' }}
    </div>
    <div v-if="message.role === 'user'" class="content">
      {{ message.content }}
    </div>
    <div v-else class="content code-content" v-html="formattedContent" @click="handleContentClick" />
  </div>
</template>

<script>
import { computed } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import { marked } from 'marked'

const highlightCode = (code, language) => {
  const normalized = (language || '').toLowerCase()
  if (normalized && hljs.getLanguage(normalized)) {
    return hljs.highlight(code, { language: normalized }).value
  }
  return hljs.highlightAuto(code).value
}

const safeEncode = (text) => encodeURIComponent(text || '')

marked.setOptions({
  gfm: true,
  breaks: true
})

const renderer = new marked.Renderer()
renderer.code = (token) => {
  const language = token.lang || 'plaintext'
  const source = token.text || ''
  const highlighted = highlightCode(source, language)
  return `
    <div class="code-block">
      <div class="code-header">
        <span class="code-lang">${language}</span>
        <button class="copy-btn" data-code="${safeEncode(source)}">复制代码</button>
      </div>
      <pre><code class="hljs language-${language}">${highlighted}</code></pre>
    </div>
  `
}

export default {
  props: {
    message: {
      type: Object,
      required: true
    }
  },
  
  setup(props) {
    const messageClass = computed(() => ({
      'user-message': props.message.role === 'user',
      'assistant-message': props.message.role === 'assistant',
      'system-message': props.message.role === 'system'
    }))

    const formattedContent = computed(() => {
      return marked.parse(props.message.content || '', { renderer })
    })

    const handleContentClick = async (event) => {
      const button = event.target.closest('.copy-btn')
      if (!button) return

      const code = decodeURIComponent(button.dataset.code || '')
      try {
        await navigator.clipboard.writeText(code)
        button.textContent = '已复制'
        setTimeout(() => {
          button.textContent = '复制代码'
        }, 1200)
      } catch (error) {
        console.error('复制失败:', error)
        button.textContent = '复制失败'
      }
    }

    return {
      messageClass,
      formattedContent,
      handleContentClick
    }
  }
}
</script>

<style scoped>
.avatar {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
}

.user-message {
  flex-direction: row-reverse;
}

.content {
  padding: 0.75rem 1rem;
  border-radius: 10px;
  max-width: 80%;
  white-space: pre-wrap;
}

.user-message .content {
  background: var(--color-primary);
  color: white;
}

.assistant-message .content {
  background: #152238;
  border: 1px solid var(--color-border);
}

.system-message .content {
  background: var(--color-danger-soft);
  color: #ffd4d8;
}

.code-block {
  margin: 1rem 0;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #2f3c54;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #1c2a43;
  color: #e0e0e0;
}

.code-lang {
  font-size: 0.85rem;
  text-transform: uppercase;
  font-family: 'Fira Code', monospace;
}

.copy-btn {
  background: #2a3d5d;
  border: 1px solid #3e5478;
  color: #e0e0e0;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: #324a72;
}

.code-content :deep(pre) {
  background: #0f1727;
  margin: 0;
  padding: 1rem;
  overflow-x: auto;
}

.code-content :deep(code) {
  font-family: 'Fira Code', Consolas, Monaco, 'Andale Mono', monospace;
  font-size: 0.9em;
  line-height: 1.4;
}

.code-content :deep(p) {
  margin: 0.5rem 0;
}

.code-content :deep(code:not(.hljs)) {
  background: rgba(0,0,0,0.06);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.assistant-message .content {
  background: #152238;
}

.code-content :deep(.hljs) {
  background: transparent;
}
</style> 