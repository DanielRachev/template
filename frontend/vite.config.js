import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const isDev = command === 'serve';

  return {
    plugins: [react()],
    base: isDev ? '' : '/static/',
    build: {
      // eslint-disable-next-line no-undef
      outDir: resolve(__dirname, '../backend/static/dist'),
      emptyOutDir: true,
      manifest: true,
      rollupOptions: {
        input: {
          // eslint-disable-next-line no-undef
          main: resolve(__dirname, 'index.html'),
        },
        output: {
          chunkFileNames: 'assets/[name]-[hash].js',
          entryFileNames: 'assets/[name]-[hash].js',
          assetFileNames: ({ name }) => {
            if (/\.css$/.test(name ?? '')) {
              return 'assets/[name]-[hash][extname]';
            }
            return 'assets/[name]-[hash][extname]';
          },
        },
      },
    },
  };
});
