import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';
// import path from 'path'; // path 모듈 임포트 제거

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vuetify({
      autoImport: true,
    }),
  ],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
    },
  },
  // resolve: { // @ 별칭 설정 제거
  //   alias: {
  //     '@': path.resolve(__dirname, './src'),
  //   },
  // },
});
