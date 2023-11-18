<template>
  <div v-if="posts" class="container">
    <h1>게시글 수정 정보</h1>
    <p>{{ posts.id }} 번 글</p>
    <h4>{{ posts.title }}</h4>
    <hr />
    <p>작성일 : {{ posts.created_at }}</p>
    <p>수정일 : {{ posts.updated_at }}</p>
    <hr />
    {{ posts.content }}
    <button @click="delPost">게시글삭제</button>
    <RouterLink
      v-if="authStore.user.pk === posts.user.pk"
      :to="{ name: 'update', params: posts.id }"
      >수정</RouterLink
    >
    <button v-if="authStore.user.pk === posts.user.pk" @click="delPost">
      삭제
    </button>
    <hr />
    <form @submit.prevent="submitComment">
      <label for="detailPostContent">내용</label>
      <input type="text" id="detailPostContent" v-model.trim="inputContent" />
      <button>댓글 작성</button>
    </form>
    <p v-for="comment in posts.comment_set" :key="comment.id">
      {{ comment.user.username }}
      {{ comment.content }}
      <button @click="delComment(comment.id)">삭제</button>
    </p>
    <hr />
    <p></p>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import { RouterLink, RouterView } from "vue-router";
import axios from "axios";
import router from "../router";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const route = useRoute();
const posts = ref(null);
const inputContent = ref("");

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/community/articles/${route.params.postId}`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      posts.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
});

const submitComment = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/community/articles/${route.params.postId}/comments/`,
    data: {
      content: inputContent.value,
    },
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      const { id, content, created_at, article, user } = res.data;
      posts.value.comment_set.push({
        id,
        content,
        created_at,
        article,
        user,
      });
      inputContent.value = "";
    })
    .catch((err) => {
      console.log(err);
    });
};

const delPost = () => {
  axios({
    method: "delete",
    url: `${authStore.API_URL}/community/articles/${route.params.postId}`,
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

const delComment = (id) => {
  axios({
    method: "delete",
    url: `${authStore.API_URL}/community/comments/${id}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then(() => {
      const idx = posts.value.comment_set.findIndex((item) => item.id === id);
      posts.value.comment_set.splice(idx, 1);
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
.container {
  border: 1px solid lightgray;
  border-radius: 5px;
}
</style>
