<template>
  <div class="container">
    <h1 class="my-3">게시글 생성 페이지</h1>
    <form @submit.prevent="submitPost">
      <label for="postTitle">제목:</label>
      <br />
      <input type="text" id="postTitle" v-model="title" />
      <br />
      <label for="postContent">내용:</label>
      <br />
      <textarea id="postContent" cols="30" rows="10" v-model="content" />
      <button class="btn btn-primary px-5">게시글 생성</button>
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const title = ref("");
const content = ref("");

const submitPost = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/community/articles/`,
    data: {
      title: title.value,
      content: content.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      router.push({ name: "post" });
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
input,
select,
textarea,
form,
button {
  width: 100%;
  border: 1px solid lightgray;
  border-radius: 5px;
}

form {
  border: 1px solid lightgray;
  padding: 20px;
}
</style>
