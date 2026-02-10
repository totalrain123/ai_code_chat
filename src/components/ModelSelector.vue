<template>
  <div class="model-selector">
    <select 
      :value="modelValue"
      :disabled="disabled"
      @input="$emit('update:modelValue', $event.target.value)"
    >
      <option v-if="models.length === 0" value="" disabled>
        暂无可用模型
      </option>
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
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue']
}
</script> 