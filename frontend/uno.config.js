import { defineConfig, presetUno, presetAttributify, presetIcons } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      collections: {
        ri: () => import('@iconify-json/ri/icons.json').then(i => i.default)
      }
    })
  ],
  theme: {
    colors: {
      // 引用 global.css 中的 CSS 变量（单一事实来源）
      'primary': 'var(--c-primary)',
      'primary-light': 'var(--c-primary-light)',
      'primary-dark': 'var(--c-primary-dark)',
      'primary-darker': 'var(--c-primary-darker)',
      'accent': 'var(--c-accent)',
      'warning': 'var(--c-warning)',
      'danger': 'var(--c-danger)',
      'success': 'var(--c-success)',
      'bg-surface': 'var(--c-bg-surface)',
      'bg-canvas': 'var(--c-bg-canvas)',
    },
    fontFamily: {
      sans: 'var(--font-sans)',
      serif: 'var(--font-serif)',
      mono: 'var(--font-mono)',
    }
  }
})
