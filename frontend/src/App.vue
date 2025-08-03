<script setup>
// ~\COPIN\frontend\src\App.vue
</script>

<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/articles">Articles</router-link>
  </nav>
  <router-view></router-view> <!-- ルーティングされたコンポーネントを表示 -->
</template>


<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
