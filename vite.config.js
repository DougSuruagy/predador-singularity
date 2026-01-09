import { defineConfig } from 'vite'

export default defineConfig({
    root: '.',
    build: {
        outDir: 'dist',
        minify: 'esbuild',
        sourcemap: false,
        rollupOptions: {
            input: {
                main: './index.html'
            }
        }
    },
    server: {
        port: 3000,
        host: true
    },
    preview: {
        port: 4173,
        host: true
    }
})
