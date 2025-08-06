import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)
app.use(router) // ルーターをアプリケーションに登録
app.mount('#app') // アプリケーションをマウント
axios.defaults.withCredentials = true