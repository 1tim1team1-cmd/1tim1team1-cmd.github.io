import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://1tim1team1-cmd.github.io',
  output: 'static',
  vite: {
    css: {
      preprocessorOptions: {}
    }
  }
});