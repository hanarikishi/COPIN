// ~/COPIN/frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue'
import Articles from '@/views/Articles.vue'

const routes = [
    { path: '/', name: 'Home', component: Home}, //Homeコンポーネントを表示するためのルート
    { path: '/articles', name: 'Articles', component: Articles}, //Articlesコンポーネントを表示するためのルート
    { path: '/article/new', name: 'NewArticle', component: () => import('../views/NewArticle.vue')}
]

// ルーターのインスタンスを作成
const router =createRouter({
    history: createWebHistory(),
    routes, // 定義したルートを使用
})

export default router // ルーターをエクスポート