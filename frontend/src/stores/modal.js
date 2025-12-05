import { defineStore } from "pinia";
import { ref } from "vue";

export const useModalStore = defineStore("modal", () => {
  // STATE
  const activeModal = ref(null);

  // ACTIONS
  const setActiveModal = (modal) => {
    activeModal.value = modal;
  };
  const closeModal = () => {
    activeModal.value = null;
  };

  return {
    activeModal,
    setActiveModal,
    closeModal,
  };
});
