<template>
  <div 
    class="message-item"
    :class="messageClass"
  >
    <div class="avatar">
      {{ message.role === 'user' ? '👤' : '🦊' }}
    </div>
    <div class="content" v-if="message.role === 'user'">
      {{ message.content }}
    </div>
    <div class="content code-content" v-else v-html="formattedContent">
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'
import { marked } from 'marked'

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

    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value
        }
        return hljs.highlightAuto(code).value
      },
      breaks: true
    })

    const formattedContent = computed(() => {
      if (props.message.role !== 'assistant') return props.message.content
      
      // 处理代码块，添加复制按钮和语言标签
      const content = props.message.content.replace(/```(\w+)?([\s\S]+?)```/g, (match, lang, code) => {
        const language = lang || 'plaintext'
        const highlighted = hljs.highlight(code.trim(), { language }).value
        return `
          <div class="code-block">
            <div class="code-header">
              <span class="code-lang">${language}</span>
              <button class="copy-btn" data-code="${encodeURIComponent(code.trim())}">
                复制代码
              </button>
            </div>
            <pre><code class="hljs language-${language}">${highlighted}</code></pre>
          </div>
        `
      })
      
      return marked(content)
    })

    // 添加复制功能
    onMounted(() => {
      document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.copy-btn')
        if (!btn) return

        const code = decodeURIComponent(btn.dataset.code)
        try {
          await navigator.clipboard.writeText(code)
          btn.textContent = '已复制！'
          setTimeout(() => {
            btn.textContent = '复制代码'
          }, 2000)
        } catch (err) {
          console.error('复制失败:', err)
          btn.textContent = '复制失败'
        }
      })
    })

    return {
      messageClass,
      formattedContent
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
  border-radius: 8px;
  max-width: 80%;
  white-space: pre-wrap;
}

.user-message .content {
  background: var(--primary-color);
  color: white;
}

.assistant-message .content {
  background: #f8f9fa;
}

.system-message .content {
  background: #fee2e2;
  color: #991b1b;
}

/* 代码块容器 */
.code-block {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #2d2d2d;
}

/* 代码头部 */
.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #2d2d2d;
  color: #e0e0e0;
}

.code-lang {
  font-size: 0.85rem;
  text-transform: uppercase;
  font-family: 'Fira Code', monospace;
}

.copy-btn {
  background: #404040;
  border: none;
  color: #e0e0e0;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: #505050;
}

/* 代码块样式 */
.code-content :deep(pre) {
  background: #1e1e1e;
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

/* 行内代码样式 */
.code-content :deep(code:not(.hljs)) {
  background: rgba(0,0,0,0.06);
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

/* 暗色主题适配 */
.assistant-message .content {
  background: #f8f9fa;
}

.code-content :deep(.hljs) {
  background: transparent;
}
</style> 