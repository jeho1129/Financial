<template>
  <dialog @click="closeModal" ref="logInDom">
    <div class="position-relative p-4 heightFull">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeLoginDialog">
          <font-awesome-icon :icon="['fas', 'xmark']" class="closeLoginDialog" />
        </button>
      </form>
      <h2 class="text-center">로그인</h2>
      <form @submit.prevent="logIn" class="d-flex flex-column gap-3" id="logInForm">
        <div>
          <label for="logInId"
            >아이디
            <span>*</span>
          </label>
          <br />
          <input v-model.trim="logInId" type="text" style="width: 100%" id="logInId" />
        </div>
        <div>
          <label for="logInPw"
            >비밀번호
            <span>*</span>
          </label>
          <br />
          <input v-model.trim="logInPw" type="password" style="width: 100%" id="logInPw" autoComplete="off" />
        </div>
        <button id="logInCk" class="px-4 py-2 mt-2">로그인</button>
      </form>
      <hr />
      <div class="text-center">
        계정이 없으신가요?
        <span @click="moveSignUp" id="moveSignUp">가입하기</span>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const logInDom = ref(null);

const logInId = ref("");
const logInPw = ref("");

const resetData = () => {
  logInId.value = "";
  logInPw.value = "";
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    logInDom.value.close();
    resetData();
  }
};

const moveSignUp = () => {
  logInDom.value.close();
  const dialog = document.querySelector("#moveSignUpPage");
  dialog.showModal();
  resetData();
};

const logIn = () => {
  const payload = {
    username: logInId.value,
    password: logInPw.value,
  };
  const dialog = document.querySelector("#moveLogInPage");
  dialog.close();
  authStore.logIn(payload);
  resetData();
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

span {
  color: darkblue;
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

#logInForm {
  margin: 0 auto;
  padding: 20px 20px 0;
  border-radius: 5px;
}

#logInCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bold;
}

#closeLoginDialog {
  border: 0px;
  background-color: transparent;
}

.closeLoginDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
