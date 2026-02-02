import react from '@vitejs/plugin-react-swc';
import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            app: resolve(__dirname, './frontend/app'),
        },
    },
    server: {
        host: '0.0.0.0',
        port: 5173,
    },
});

