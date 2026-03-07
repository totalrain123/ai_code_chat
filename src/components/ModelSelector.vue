<template>
  <div class="model-selector">
    <select
      :value="modelValue"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option
        v-for="model in models"
        :key="model.id"
        :value="model.id"
      >
        {{ model.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    models: {
      type: Array,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue']
}
</script> 

<style scoped>
.model-selector select {
  border: 1px solid var(--color-border);
  background: #152238;
  color: var(--color-text);
  border-radius: 9px;
  padding: 0.5rem 0.65rem;
  min-width: 170px;
}
</style>