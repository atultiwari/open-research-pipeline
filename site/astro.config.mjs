// @ts-check
import { defineConfig } from 'astro/config';

// Project page on GitHub Pages: https://atultiwari.github.io/open-research-pipeline/
export default defineConfig({
  site: 'https://atultiwari.github.io',
  base: '/open-research-pipeline',
  trailingSlash: 'always',
  output: 'static',
});
