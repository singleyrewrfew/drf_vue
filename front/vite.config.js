import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import compression from 'vite-plugin-compression'

export default defineConfig({
    plugins: [
        vue(),
        // Gzip 压缩配置
        compression({
            algorithm: 'gzip',
            ext: '.gz',
            threshold: 10240, // 大于 10KB 才压缩
            deleteOriginFile: false,
            filter: /\.(js|css|html|svg)$/
        }),
        // Brotli 压缩配置（更高效的压缩算法）
        compression({
            algorithm: 'brotliCompress',
            ext: '.br',
            threshold: 10240,
            deleteOriginFile: false,
            filter: /\.(js|css|html|svg)$/
        })
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, 'src')
        }
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    'element-plus': ['element-plus'],
                    'vendor': ['vue', 'vue-router', 'pinia', 'axios']
                }
            }
        },
        chunkSizeWarningLimit: 1000,
        cssCodeSplit: true
    },
    server: {
        port: 3000,
        strictPort: false,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true
            },
            '/media': {
                target: 'http://localhost:8000',
                changeOrigin: true
            }
        }
    }
})
