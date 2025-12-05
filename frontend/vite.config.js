// vite.config.js
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "node:path";

const varsPath = path.resolve(__dirname, "src/assets/styles/_vars.scss");

const HOST = "http://127.0.0.1:8000";
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "^/api": {
        target: HOST,
        ws: true,
        changeOrigin: true,
      },
    },
  },
});
