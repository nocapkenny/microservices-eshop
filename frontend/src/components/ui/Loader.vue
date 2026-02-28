<template>
  <div class="loader-container" :class="`loader-container--${size}`">
    <div class="pulse-loader">
      <span></span>
      <span></span>
      <span></span>
    </div>
    <p v-if="text" class="loader-text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  text: {
    type: String,
  },
  size: {
    type: String,
    default: "md",
  },
});
</script>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.loader-container--sm .pulse-loader span {
  width: 12px;
  height: 12px;
}
.loader-container--md .pulse-loader span {
  width: 20px;
  height: 20px;
}
.loader-container--lg .pulse-loader span {
  width: 30px;
  height: 30px;
}

.pulse-loader {
  display: flex;
  gap: 8px;
}

.pulse-loader span {
  background-color: #2e8b57;
  border-radius: 50%;
  animation: pulse 1.4s ease-in-out infinite;
}

.pulse-loader span:nth-child(1) {
  animation-delay: 0s;
}
.pulse-loader span:nth-child(2) {
  animation-delay: 0.2s;
}
.pulse-loader span:nth-child(3) {
  animation-delay: 0.4s;
}

.loader-text {
  margin-top: 15px;
  color: #2e8b57;
  font-size: 14px;
  font-weight: 500;
}

@keyframes pulse {
  0%,
  80%,
  100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
