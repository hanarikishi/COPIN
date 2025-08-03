import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router) // ルーターをアプリケーションに登録
app.mount('#app') // アプリケーションをマウント