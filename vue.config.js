const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    proxy: {
      '/api': {
        target: 'https://jda.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
      '/websockify': {
        target: 'https://jda.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
      '/vnc': {
        target: 'https://jda.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
    }
  },
})
