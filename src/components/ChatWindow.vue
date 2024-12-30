<template>
  <div class="chat-window">
    <div class="messages" ref="messagesContainer">
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
import { ref, watch } from 'vue'
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

    watch(() => props.messages.length, () => {
      setTimeout(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      }, 100)
    })

    return {
      messagesContainer
    }
  }
}
</script> 