<script setup>
// ~/COPIN/frontend/src/views/NewArticle.vue
    import {ref} from 'vue'
    import axios from 'axios'
    import {useRouter} from 'vue-router'

    const router = useRouter()

    const title = ref('')
    const content = ref('')
    const tags = ref('')

    // 記事を登録
    const submitArticle = async() => {
        try{
            const payload = {
                title: title.value,
                content:content.value,
                tags: tags.value.split(',').map(tag => tag.trim())
            }
            const res = await axios.post('/api/articles', payload)
            router.push({ name: 'Articles' }) // 記事一覧ページにリダイレクト
            console.log('記事が登録されました:', res.data)
        } catch (error) {
            console.error('記事の登録に失敗しました:', error)
        }
    }
</script>

<template>
    <div>
        <h2>新規投稿</h2>
        <form @submit.prevent="submitArticle">
            <div>
                <label>タイトル</label> <br />
                <input v-model="title" type="text" requires />
            </div>
            <div>
                <label>本文</label>
                <textarea v-model="content" required rowa="20" cols="40" />
            </div>
            <div>
                <label>タグ</label>
                <input v-model="tags" type="text" />
            </div>
            <button type="submit">投稿</button>
            <button @click="router.push({ name: 'Articles' })">戻る</button>
        </form>
    </div>
</template>