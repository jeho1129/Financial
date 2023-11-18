<template>
  <dialog @click="closeModal" ref="postCreateDom">
    <div class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close" class="m-0">❌</button>
      </form>
      <h2 class="text-center">게시글 생성</h2>
      <form @submit.prevent="submitPost" class="d-flex flex-column gap-3">
        <div>
          <label for="postTitle">제목</label>
          <br />
          <input type="text" id="postTitle" v-model.trim="title" />
        </div>
        <div>
          <label for="postContent">내용</label>
          <br />
          <textarea
            id="postContent"
            cols="30"
            rows="10"
            v-model.trim="content"
          />
        </div>
        <button class="btn btn-primary px-5">게시글 생성</button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const postCreateDom = ref(null);

const title = ref("");
const content = ref("");
const emit = defineEmits(["someEvent"]);

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
      console.log(res.data);
      postCreateDom.value.close();
      emit("someEvent", res.data);
    })
    .catch((err) => {
      console.log(err);
    });
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    postCreateDom.value.close();
  }
};
</script>

<style scoped>
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}

dialog {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  border: 0;
  border-radius: 10px;
  padding: 0;
  width: 500px;
}

input,
select,
textarea,
button {
  width: 100%;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.move {
  right: 10px;
}
</style>
