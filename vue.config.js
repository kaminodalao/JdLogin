const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    proxy: {
      '/api': {
        target: 'https://jdlogin.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
      '/websockify': {
        target: 'https://jdlogin.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
      '/vnc': {
        target: 'https://jdlogin.myyoo.fun/',
        ws: true,
        changeOrigin: true
      },
    }
  },
})
