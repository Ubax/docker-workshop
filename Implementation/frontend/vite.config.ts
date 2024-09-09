import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tsconfigPaths from 'vite-tsconfig-paths'


// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())
  const backendUrl = env.VITE_API_BASE_URL
  const port = env.VITE_PORT ? parseInt(env.VITE_PORT) : 5173
  return {
    plugins: [vue(), vueJsx(), vueDevTools(), tsconfigPaths()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      port,
      proxy: {
        '/api': {
          target: backendUrl
        }
      }
    }
  }
})
