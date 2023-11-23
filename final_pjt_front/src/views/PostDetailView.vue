<template>
  <div v-if="posts" class="container my-4">
    <div class="defaultPostDetail p-4">
      <div class="d-flex justify-content-between">
        <h3>{{ posts.title }}</h3>
        <div class="d-flex align-items-center gap-1">
          <!-- <RouterLink v-if="authStore.user.id === posts.user.pk" :to="{ name: 'update', params: posts.id }">수정</RouterLink> -->
          <button
            v-if="authStore.user?.id === posts.user.pk"
            id="postEditButton"
            :to="{ name: 'update', params: posts.id }"
          >
            <font-awesome-icon
              :icon="['far', 'pen-to-square']"
              class="postEditButton"
            />
          </button>
          <button
            v-if="
              authStore.user?.is_superuser ||
              authStore.user?.id === posts.user.pk
            "
            @click="delPost"
            id="postDelButton"
          >
            <font-awesome-icon
              :icon="['far', 'trash-can']"
              class="postDelButton"
            />
          </button>
        </div>
      </div>
      <div class="d-flex gap-3">
        <img src="../assets/profile.jpg" alt="" />
        <div class="d-flex flex-column">
          <p class="m-0">{{ posts.user.username }}</p>
          <p class="m-0">{{ date + " " + time }}</p>
        </div>
      </div>

      <hr />
      {{ posts.content }}

      <hr />
      <p>댓글 {{ posts.comment_set.length }} ></p>
      <form @submit.prevent="submitComment" class="position-relative">
        <div v-if="authStore.user">
          <input
            type="text"
            id="detailPostContent"
            placeholder="댓글을 남겨보세요"
            v-model.trim="inputContent"
            required
          />
          <button id="submitCommentBtn">
            <font-awesome-icon :icon="['fas', 'pen']" />
          </button>
        </div>
        <div v-else>
          <input
            type="text"
            id="detailPostContent"
            placeholder="로그인 후 댓글 작성이 가능해요"
            readonly
          />
        </div>
      </form>
      <template v-if="posts.comment_set.length">
        <div
          v-for="comment in posts.comment_set"
          :key="comment.id"
          class="d-flex align-items-center justify-content-between my-3"
        >
          <div>
            <p class="m-0">{{ comment.user.username }}</p>
            <p class="m-0">{{ comment.content }}</p>
            <p class="m-0">
              {{
                new Date(
                  new Date(comment.created_at).getTime() + 9 * 60 * 60 * 1000
                )
                  .toISOString()
                  .split("T")[0] +
                " " +
                new Date(comment.created_at).toTimeString().split(" ")[0]
              }}
            </p>
          </div>
          <div class="d-flex align-items-center gap-1">
            <button
              v-if="authStore.user?.id === comment.user.pk"
              id="postEditButton"
              :to="{ name: 'update', params: posts.id }"
            >
              <font-awesome-icon
                :icon="['far', 'pen-to-square']"
                class="postEditButton"
              />
            </button>
            <button
              v-if="
                authStore.user?.is_superuser ||
                authStore.user?.id === comment.user.pk
              "
              @click="delComment(comment.id)"
              id="commentDelButton"
            >
              <font-awesome-icon
                :icon="['far', 'trash-can']"
                class="commentDelButton"
              />
            </button>
          </div>
        </div>
      </template>
      <div
        v-else
        class="my-3 d-flex flex-column align-items-center text-secondary m-5"
      >
        <p class="m-0 fs-1">
          <font-awesome-icon :icon="['far', 'comment-dots']" />
        </p>
        <p class="m-0">등록된 댓글이 없습니다</p>
      </div>
      <hr />
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
  })
    .then((res) => {
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
  width: 50px;
  height: 50px;
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

#postDelButton,
#commentDelButton {
  border: 2px solid red;
  border-radius: 5px;
  background-color: white;
}

.postDelButton,
.commentDelButton {
  color: red;
}
#postEditButton {
  border: 2px solid #5fb9a6;
  border-radius: 5px;
  background-color: white;
}

.postEditButton {
  color: #5fb9a6;
}

#detailPostContent {
  border: 1px solid lightgray;
  border-radius: 5px;
  width: 100%;
  padding: 20px 10px;
}

#submitCommentBtn {
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0px;
  border: 0px;
  font-size: larger;
  background-color: transparent;
  color: #5fb9a6;
  font-weight: bold;
}
</style>
