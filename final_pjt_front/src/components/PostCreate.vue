<template>
  <dialog @click="closeModal" ref="postCreateDom">
    <div class="position-relative p-4 heightFull">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closePostCreateDialog">
          <font-awesome-icon
            :icon="['fas', 'xmark']"
            class="closePostCreateDialog"
          />
        </button>
      </form>
      <h2 class="text-center">게시글 생성</h2>
      <form
        @submit.prevent="submitPost"
        class="d-flex flex-column gap-3"
        id="postCreateForm"
      >
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
            rows="7"
            v-model.trim="content"
          />
        </div>
        <button id="postCreateCk" class="px-4 py-2 mt-2">게시글 생성</button>
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

const resetData = () => {
  title.value = "";
  content.value = "";
};

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
      postCreateDom.value.close();
      resetData();
      emit("someEvent", res.data);
    })
    .catch((err) => {
      console.log(err);
    });
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    postCreateDom.value.close();
    resetData();
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
  height: 500px;
  width: 500px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.move {
  top: 20px;
  right: 20px;
}

.heightFull {
  height: 100%;
}

#postCreateForm {
  margin: 0 auto;
  padding: 20px 20px 0;
  border-radius: 5px;
}

#postCreateCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bold;
}

#closePostCreateDialog {
  border: 0px;
  background-color: transparent;
}

.closePostCreateDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
