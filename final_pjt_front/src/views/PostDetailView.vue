<template>
  <div v-if="posts" class="container my-4">
    <div class="defaultPostDetail p-4">
      <h3>{{ posts.title }}</h3>
      <p>작성자 : {{ posts.user.username }}</p>
      <p>작성일 : {{ date + " " + time }}</p>
      <hr />
      {{ posts.content }}
      <button v-if="authStore.user.id === posts.user.pk" @click="delPost">
        게시글삭제
      </button>
      <!-- <RouterLink v-if="authStore.user.id === posts.user.pk" :to="{ name: 'update', params: posts.id }">수정</RouterLink> -->
      <button
        v-if="authStore.user.id === posts.user.pk"
        :to="{ name: 'update', params: posts.id }"
      >
        수정
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
        <button
          v-if="authStore.user.id === comment.user.pk"
          @click="delComment(comment.id)"
        >
          삭제
        </button>
      </p>
      <hr />
      <div>
        <img src="../assets/profile.jpg" alt="" />

        <hr />
      </div>
    </div>
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
const date = ref("");
const time = ref("");

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
      const TIME_ZONE = 9 * 60 * 60 * 1000; // 9시간
      const d = new Date(res.data.created_at);

      date.value = new Date(d.getTime() + TIME_ZONE)
        .toISOString()
        .split("T")[0];
      time.value = d.toTimeString().split(" ")[0];
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
  width: 700px;
}

.defaultPostDetail {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

img {
  width: 60px;
  border-radius: 50%;
}

#moveProfileEdit {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

#moveProfileEdit:hover {
  filter: brightness(0.9);
}
</style>
