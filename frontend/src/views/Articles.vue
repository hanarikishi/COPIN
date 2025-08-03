<script setup>
    // ~\COPIN\frontend\src\views\Articles.vue
    import {ref, onMounted } from 'vue'
    import axios from 'axios'

    const articles = ref([]) // 記事のリストを保持するリアクティブな変数

    // コンポーネントがマウントされたときに記事を取得
    onMounted(async () => {
        console.log('onMounted 実行')
        try {
            const res = await axios.get('/api/articles') // APIエンドポイントから記事を取得
            articles.value = res.data
            console.log('保存されてる記事データ', articles.value)
            console.log('取得した記事データ', articles.value)
        } catch (error) {
            console.error('記事の取得に失敗しました。',error)
        }

    })
</script>
<template>
    <div>
        <h2>記事一覧</h2>
        <ul>
            <li v-for="a in articles" :key="a.id">
                <strong>{{ a.title }}</strong><br />
                投稿者: {{ a.author }}<br />
                タグ: <span v-for="t in a.tags" :key="t">{{ t }}</span><br />
                投稿日: {{ a.created_at }}
            </li>
        </ul>
    </div>
</template>