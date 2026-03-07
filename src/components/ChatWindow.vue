<template>
  <div ref="messagesContainer" class="chat-window">
    <div class="messages">
      <MessageItem
        v-for="(message, index) in messages"
        :key="index"
        :message="message"
      />
      <div v-if="loading" class="loading-indicator">
        AI正在思考...
      </div>
    </div>
  </div>
</template>

<script>
import { nextTick, ref, watch } from 'vue'
import MessageItem from './MessageItem.vue'

export default {
  components: {
    MessageItem
  },
  props: {
    messages: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const messagesContainer = ref(null)

    const scrollToBottom = async () => {
      await nextTick()
      if (!messagesContainer.value) return
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }

    watch(() => props.messages.length, scrollToBottom)
    watch(() => props.loading, scrollToBottom)

    return {
      messagesContainer
    }
  }
}
</script> 