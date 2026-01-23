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
      'police-blue': '#1e3a8a',
      'police-light': '#3b82f6'
    }
  }
})
