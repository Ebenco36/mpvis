// const IS_PRODUCTION = process.env.NODE_ENV === 'production'
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  pages: {
    index: {
      entry: 'src/pages/main.js', // Change the entry file path here
      template: 'public/index.html',
      filename: 'index.html',
    },
  },
  outputDir: 'dist',
  assetsDir: 'static',
  // baseUrl: IS_PRODUCTION
  // ? 'http://cdn123.com'
  // : '/',
  // For Production, replace set baseUrl to CDN
  // And set the CDN origin to `yourdomain.com/static`
  // Whitenoise will serve once to CDN which will then cache
  // and distribute
  devServer: {
    proxy: {
      '/api*': {
        // Forward frontend dev server request for /api to django dev server
        target: 'http://localhost:8000/',
        changeOrigin: true,
      }
    }
  },
  transpileDependencies: true,
})

// module.exports = {
//   pages: {
//     index: {
//       entry: 'pages/main.js', // Change the entry file path here
//       template: 'public/index.html',
//       filename: 'index.html',
//     },
//   },
//   outputDir: 'dist',
//   assetsDir: 'static',
//   // baseUrl: IS_PRODUCTION
//   // ? 'http://cdn123.com'
//   // : '/',
//   // For Production, replace set baseUrl to CDN
//   // And set the CDN origin to `yourdomain.com/static`
//   // Whitenoise will serve once to CDN which will then cache
//   // and distribute
//   devServer: {
//     proxy: {
//       '/api*': {
//         // Forward frontend dev server request for /api to django dev server
//         target: 'http://localhost:8000/'
//       }
//     }
//   }
// }
