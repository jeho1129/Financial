<template>
  <div class="container">
    <h1>게시글 목록 페이지</h1>
    <RouterLink to="/postCreate">게시글 생성</RouterLink>
    <div v-for="post in posts" :key="post.id" class="mx-5" @click="detailPost(post.id)">
      <p>{{ post.id }}번 글 | {{ post.title }}</p>
      <hr />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import axios from "axios";

const router = useRouter();
const posts = ref([]);

const detailPost = (id) => {
  router.push({ name: "postDetail", params: { postId: id } });
};

onMounted(() => {
  axios({
    method: "get",
    url: "http://127.0.0.1:8000/community/articles/",
  })
    .then((res) => {
      posts.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>

<style scoped></style>
