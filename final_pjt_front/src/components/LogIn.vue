<template>
  <dialog @click="closeModal" ref="logIn">
    <div id="hhh" class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close">❌</button>
      </form>
      <h2 class="text-center">로그인</h2>
      <form class="d-flex flex-column gap-3">
        <div>
          <label for="LogInId"
            >아이디
            <span>*</span>
          </label>
          <br />
          <input type="text" style="width: 100%" id="LogInId" />
        </div>
        <div>
          <label for="LogInMail"
            >비밀번호
            <span>*</span>
          </label>
          <br />
          <input type="password" style="width: 100%" id="LogInPw" autoComplete="off" />
        </div>
        <button class="btn btn-primary">로그인</button>
      </form>
      <hr />
      <div class="text-center">계정이 없으신가요? <span @click="moveSignUp" id="moveSignUp" class="text-primary">가입하기</span></div>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
const logIn = ref(null);

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    logIn.value.close();
  }
};

const moveSignUp = () => {
  logIn.value.close();
  const dialog = document.querySelector("#moveSignUpPage");
  dialog.showModal();
};
</script>

<style scoped>
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}
dialog {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  border: 0;
  border-radius: 20px;
  padding: 0;
  height: 500px;
  width: 500px;
}

span {
  color: darkblue;
}

.move {
  right: 10px;
}

#hhh {
  height: 100%;
}

#moveSignUp {
  cursor: pointer;
  font-weight: bold;
}
</style>
