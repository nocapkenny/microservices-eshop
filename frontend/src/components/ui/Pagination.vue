<script setup>
const props = defineProps({
  pages: {
    type: Number,
    required: true,
  },
  modelValue: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(["update:modelValue"]);
</script>

<template>
  <section class="pagination" v-auto-animate>
    <button
      class="pagination__btn"
      v-for="page in props.pages"
      :key="page"
      :class="{ active: page === props.modelValue }"
      @click="$emit('update:modelValue', page)"
    >
      {{ page }}
    </button>
  </section>
</template>

<style lang="scss" scoped>
.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  &__btn {
    transition: all 0.3s ease;
  }
  &__btn:hover,
  &__btn.active {
    background-color: #2e8b57;
    color: #fff;
  }
}
</style>
