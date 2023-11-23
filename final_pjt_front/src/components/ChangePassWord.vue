<template>
  <dialog @click="closeModal" ref="changePassWordDom">
    <div class="position-relative p-4 heightFull">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeChangePassWordDialog">
          <font-awesome-icon
            :icon="['fas', 'xmark']"
            class="closeChangePassWordDialog"
          />
        </button>
      </form>
      <h2 class="text-center">비밀번호 변경</h2>
      <form
        @submit.prevent="changePassword"
        class="d-flex flex-column gap-3"
        id="changePassWordForm"
      >
        <div>
          <label for="passWord">새 비밀번호 </label>
          <br />
          <input
            v-model.trim="passWord"
            type="password"
            style="width: 100%"
            id="passWord"
            autoComplete="off"
            required
          />
        </div>
        <p class="m-0 text-danger" style="display: none" ref="notSuccess">
          비밀번호를 확인해주세요
        </p>
        <div>
          <label for="passWordCk">새 비밀번호 확인 </label>
          <br />
          <input
            v-model.trim="passWordCk"
            type="password"
            style="width: 100%"
            id="passWordCk"
            autoComplete="off"
            required
          />
        </div>
        <button id="changePassWordCk" class="px-4 py-2 mt-2">
          비밀번호 변경
        </button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const authStore = useAuthStore();
const changePassWordDom = ref(null);

const passWord = ref("");
const passWordCk = ref("");
const notSuccess = ref(null);

const resetData = () => {
  notSuccess.value.style.display = "none";
  passWord.value = "";
  passWordCk.value = "";
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    changePassWordDom.value.close();
    resetData();
  }
};

const changePassword = () => {
  if (window.confirm("비밀번호 변경을 하시겠습니까?")) {
    if (passWord.value === passWordCk.value) {
      axios({
        method: "put",
        url: `${authStore.API_URL}/accounts/user/ `,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
        data: {
          password1: passWord.value,
          password2: passWordCk.value,
        },
      })
        .then((res) => {
          notSuccess.value.style.display = "none";
          const dialog = document.querySelector("#moveChangePassWord");
          dialog.close();
          resetData();
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      notSuccess.value.style.display = "block";
    }
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

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.move {
  top: 20px;
  right: 20px;
}

#moveSignUp {
  cursor: pointer;
  font-weight: bold;
  color: #5fb9a6;
}

.heightFull {
  height: 100%;
}

#changePassWordForm {
  margin: 0 auto;
  padding: 20px 20px 0;
  border-radius: 5px;
}

#changePassWordCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bolder;
}

#closeChangePassWordDialog {
  border: 0px;
  background-color: transparent;
}

.closeChangePassWordDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
