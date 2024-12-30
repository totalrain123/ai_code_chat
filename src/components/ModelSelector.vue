<template>
  <div class="model-selector">
    <select 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
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