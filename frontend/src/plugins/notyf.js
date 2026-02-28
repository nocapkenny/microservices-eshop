import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';

export const notyf = new Notyf({
  duration: 3000,
  position: {
    x: 'right',
    y: 'top',
  },
  dismissible: true,
  types: [
    {
      type: 'warning',
      background: 'orange',
      icon: {
        className: 'fas fa-exclamation-triangle',
        tagName: 'i',
      }
    }
  ]
});

export default {
  install: (app) => {
    app.config.globalProperties.$notyf = notyf;
  }
};