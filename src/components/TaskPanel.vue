<template>
  <div class="task-panel" :class="{ 'is-open': isOpen }">
    <div class="task-header">
      <h2>任务管理</h2>
      <button class="close-btn" @click="handleClose" title="关闭">×</button>
    </div>
    <div class="task-content">
      <form class="new-task-form" @submit.prevent="createNewTask">
        <input v-model="newTitle" placeholder="任务标题" required />
        <input v-model="newDesc" placeholder="任务描述" />
        <button type="submit">添加</button>
      </form>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="tasks.length === 0" class="empty">暂无任务</div>
      <ul v-else class="task-list">
        <li v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-main">
            <span class="task-title">{{ task.title }}</span>
            <span class="task-status">{{ task.status }}</span>
          </div>
          <div class="task-desc">{{ task.description }}</div>
          <button v-if="task.status !== 'done'" @click="markDone(task.id)">完成</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { createTask, getTasks, updateTaskStatus } from '../services/api'

export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const tasks = ref([])
    const loading = ref(false)
    const newTitle = ref('')
    const newDesc = ref('')

    const handleClose = () => {
      emit('close')
    }

    const loadTasks = async () => {
      loading.value = true
      try {
        tasks.value = await getTasks()
      } catch (e) {
        console.error('加载任务失败', e)
      } finally {
        loading.value = false
      }
    }

    const createNewTask = async () => {
      if (!newTitle.value.trim()) return
      try {
        const task = await createTask({ title: newTitle.value, description: newDesc.value })
        tasks.value.unshift(task)
        newTitle.value = ''
        newDesc.value = ''
      } catch (e) {
        console.error('创建任务失败', e)
      }
    }

    const markDone = async (id) => {
      try {
        const task = await updateTaskStatus(id, 'done')
        const index = tasks.value.findIndex(t => t.id === id)
        if (index > -1) tasks.value[index] = task
      } catch (e) {
        console.error('更新任务状态失败', e)
      }
    }

    onMounted(() => {
      loadTasks()
    })

    return { tasks, loading, newTitle, newDesc, handleClose, createNewTask, markDone }
  }
}
</script>

<style scoped>
.task-panel {
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

.task-panel.is-open {
  right: 0;
}

.task-header {
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

.task-content {
  height: calc(100vh - 60px);
  overflow-y: auto;
  padding: 1rem;
}

.new-task-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.new-task-form input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.new-task-form button {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.75rem;
}

.task-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.25rem;
}

.task-title {
  font-weight: bold;
}

.task-status {
  font-size: 0.875rem;
  color: var(--primary-color);
}

.task-desc {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.task-item button {
  padding: 0.25rem 0.75rem;
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-item button:hover {
  opacity: 0.9;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
