<template>
  <dialog @click="closeModal" ref="signUpDom">
    <div class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close" class="m-0">❌</button>
      </form>
      <h2 class="text-center">회원가입</h2>
      <form @submit.prevent="signUp">
        <div class="d-flex flex-column gap-3">
          <h5 class="m-0">기본정보</h5>
          <div>
            <label for="signUpId"
              >아이디
              <span>*</span>
            </label>
            <br />
            <input type="text" v-model="signUpId" id="signUpId" style="width: 100%" required />
          </div>
          <div>
            <label for="signUpPw"
              >비밀번호
              <span>*</span>
            </label>
            <br />
            <input type="password" v-model="signUpPw" id="signUpPw" autoComplete="off" style="width: 100%" required />
          </div>
          <div>
            <label for="signUpPwCk"
              >비밀번호 재확인
              <span>*</span>
            </label>
            <br />
            <input type="password" v-model="signUpPwCk" id="signUpPwCk" autoComplete="off" style="width: 100%" required />
          </div>
          <div class="d-flex gap-3">
            <div style="width: 70%">
              <label for="signUpName"
                >이름
                <span>*</span>
              </label>
              <br />
              <input type="text" v-model="signUpName" id="signUpName" style="width: 100%" required />
            </div>
            <div style="width: 30%">
              <label for="signUpAge"
                >나이
                <span>*</span>
              </label>
              <br />
              <input type="number" v-model="signUpAge" id="signUpAge" style="width: 100%" required />
            </div>
          </div>
          <div>
            <label for="signUpMail">이메일 </label>
            <br />
            <input type="email" v-model="signUpEmail" id="signUpMail" style="width: 100%" />
          </div>
        </div>
        <hr />
        <div class="d-flex flex-column gap-3">
          <h5 class="m-0">추가정보</h5>
          <div>
            <label for="signUpMoney">자산</label>
            <br />
            <input type="text" v-model="signUpMoney" id="signUpMoney" style="width: 100%" />
          </div>
          <div>
            <label for="signUpSalary">연봉</label>
            <br />
            <input type="password" v-model="signUpSalary" id="signUpSalary" autoComplete="off" style="width: 100%" />
          </div>
        </div>
        <button class="btn btn-primary position-sticky">회원가입</button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";

const signUpDom = ref(null);
const signUpId = ref(null);
const signUpPw = ref(null);
const signUpPwCk = ref(null);
const signUpName = ref(null);
const signUpAge = ref(null);
const signUpEmail = ref(null);
const signUpMoney = ref(null);
const signUpSalary = ref(null);

const authStore = useAuthStore();

const signUp = function () {
  const payload = {
    password1: signUpPw.value,
    password2: signUpPwCk.value,
    username: signUpId.value,
    name: signUpName.value,
    email: signUpEmail.value,
    age: signUpAge.value,
    asset: signUpMoney.value,
    salary: signUpSalary.value,
  };
  authStore.signUp(payload);
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    signUpDom.value.close();
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

input {
  border-radius: 5px;
  border: 1px solid black;
}

button {
  margin-top: 24px;
  width: 100%;
  bottom: 24px;
}
</style>
