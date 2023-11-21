<template>
  <div class="container mt-5">
    <!-- <h1>게시글 목록 페이지</h1> -->
    <div class="fs-4" id="postTitle">커뮤니티</div>
    <div class="d-flex justify-content-between align-items-center my-2">
      <p class="m-0">전체 {{ posts.length }} 건</p>
      <div>
        <button
          v-show="authStore.isAuthenticated"
          @click="showModal"
          class="px-4 py-2"
        >
          글쓰기
        </button>
      </div>
    </div>
    <table class="table">
      <thead class="table-success">
        <tr>
          <th scope="col">No</th>
          <th scope="col">제목</th>
          <th scope="col">작성자</th>
          <th scope="col">작성일</th>
        </tr>
      </thead>
      <tbody>
        <tr
          @click="detailPost(post.id)"
          v-for="(post, idx) in sortPosts"
          :key="post.id"
        >
          <td>{{ posts.length - idx }}</td>
          <td>
            {{ post.title }}
            <font-awesome-icon :icon="['far', 'comment']" />
            <span style="margin-left: 2px">
              {{ post.comment_set?.length ?? 0 }}
            </span>
          </td>
          <td>{{ post.user.username }}</td>
          <td>
            {{
              new Intl.DateTimeFormat("ko-KR").format(new Date(post.created_at))
            }}
          </td>
        </tr>
      </tbody>
    </table>

    <PostCreate id="movePostCreate" @some-event="pushData" />
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { onMounted, ref, computed } from "vue";
import axios from "axios";
import PostCreate from "../components/PostCreate.vue";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const posts = ref([]);
const authStore = useAuthStore();

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
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
});

const sortPosts = computed(() => {
  return posts.value.toSorted((a, b) => b.id - a.id);
});

const pushData = (args) => {
  posts.value.push(args);
  console.log(posts.value);
};

const showModal = () => {
  const dialog = document.querySelector("#movePostCreate");
  dialog.showModal();
};
</script>

<style scoped>
#postTitle {
  color: #5fb9a6;
  font-weight: bold;
}

button {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

button:hover {
  filter: brightness(0.9);
}
</style>
