<script setup>
// ~/COPIN/frontend/src/views/NewArticle.vue
    import {ref, computed} from 'vue'
    import axios from 'axios'
    import {useRouter} from 'vue-router'

    const router = useRouter()

    const title = ref('')
    const content = ref('')
    const tags = ref('')

    // リアルタイムバリデーション
    const isValid = computed(() => {
        return title.value.trim() !== '' && content.value.trim() !== ''
    })

    // 記事を登録
    const submitArticle = async() => {
        if (!isValid.value) {
            alert('タイトルと本文は必須です。')
            return
        }
        try{
            const payload = {
                title: title.value,
                content:content.value,
                tags: tags.value.split(',').map(tag => tag.trim())
            }
            const res = await axios.post('/api/articles', payload)
            router.push({ name: 'Articles' },{withCredentials: true}) // 記事一覧ページにリダイレクト,セッション Cookie を維持
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
                <input v-model="title" type="text" placeholder="タイトルを入力" />
            </div>
            <div>
                <label>本文</label>
                <textarea v-model="content" required rows="20" cols="40" placeholder="記事の内容を入力してください"></textarea>
            </div>
            <div>
                <label>タグ</label>
                <input v-model="tags" type="text" />
            </div>
            <div>
                <p v-if="!isValid" style="color: red;">※タイトルと本文は必須です。</p>
            </div>
            <button :disabled="!isValid" type="submit">投稿</button>
            <button @click="router.push({ name: 'Articles' })">戻る</button>
        </form>
    </div>
</template>