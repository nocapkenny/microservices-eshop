<script setup>
import { ref, onMounted } from 'vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Pagination, Autoplay, EffectFade } from 'swiper/modules';
import axios from 'axios';

// Импортируем стили Swiper
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/effect-fade';

// Пропсы для гибкости
const props = defineProps({
  autoPlay: {
    type: Boolean,
    default: true
  },
  height: {
    type: String,
    default: '450px'
  },
  slides: {
    type: Array,
  }
});

</script>

<template>
  <div class="slider-wrapper" :style="{ height: props.height }">
    <Swiper
      :modules="[Navigation, Pagination, Autoplay, EffectFade]"
      :slides-per-view="1"
      :loop="true"
      :autoplay="autoPlay ? { delay: 5000, disableOnInteraction: false } : false"
      :pagination="{ clickable: true }"
      :navigation="true"
      effect="fade"
      class="my-swiper"
    >
      <SwiperSlide v-for="slide in slides" :key="slide.id">
        <div class="slide-content">
          <img :src="slide.image_url" :alt="slide.title" class="slide-image" />
          
          <div class="slide-info">
            <h3 v-if="slide.title">{{ slide.title }}</h3>
            <p v-if="slide.description">{{ slide.description }}</p>
            <a 
              v-if="slide.link" 
              :href="slide.link" 
              class="slide-btn"
              target="_blank"
            >
              Подробнее
            </a>
          </div>
        </div>
      </SwiperSlide>
    </Swiper>
  </div>
</template>

<style lang="scss">
$accent-green: #2e8b57;
$accent-red: #c22a3b;
$text: #e0e0e0;
$dark-bg: #121212;

.slider-wrapper {
  position: relative;
  width: 100%;
  margin-top: 50px;
  border-radius: 16px;
  overflow: hidden;
  background: $dark-bg;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  @media (max-width: 600px) {
    margin-top: 150px;
  }
}

.my-swiper {
  width: 100%;
  height: 100%;
}

.slide-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.slide-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px;
  background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
  color: $text;

  h3 {
    margin: 0 0 10px;
    font-size: 1.8rem;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
  }

  p {
    margin: 0 0 20px;
    font-size: 1.1rem;
    opacity: 0.95;
    max-width: 600px;
  }
}

.slide-btn {
  display: inline-block;
  padding: 12px 24px;
  background: $accent-green;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s;

  &:hover {
    background: lighten($accent-green, 10%);
    transform: translateY(-2px);
  }
}
.swiper-button-prev,
.swiper-button-next{
    display: none !important;
}

// Лоадер
.slider-loader,
.slider-error,
.slider-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: $text;
  text-align: center;
  padding: 20px;

  button {
    padding: 10px 20px;
    background: $accent-green;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    margin-top: 10px;

    &:hover {
      background: lighten($accent-green, 10%);
    }
  }
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: $accent-green;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
}

// Адаптивность
@media (max-width: 768px) {
  .slide-info {
    padding: 20px;
    
    h3 {
      font-size: 1.3rem;
    }
    p {
      font-size: 0.95rem;
    }
  }
  
  :deep(.swiper-button-next),
  :deep(.swiper-button-prev) {
    width: 40px;
    height: 40px;
  }
}
</style>