<template>
  <dialog @click="closeModal" ref="signUpDom">
    <div class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close" class="m-0" id="closeSignUpDialog">
          <font-awesome-icon :icon="['fas', 'xmark']" class="closeSignUpDialog" />
        </button>
      </form>
      <h2 class="text-center">회원가입</h2>
      <form @submit.prevent="signUp" id="signUpForm">
        <div class="d-flex flex-column gap-3">
          <h5 class="m-0">필수정보</h5>
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
              <input type="number" v-model.trim="signUpAge" id="signUpAge" style="width: 100%" required />
            </div>
          </div>
          <div>
            <label for="signUpMail">이메일 <span>*</span></label>
            <br />
            <input type="email" v-model.trim="signUpEmail" id="signUpMail" style="width: 100%" required />
          </div>
          <div>
            <label for="signUpJob">직업 <span>*</span></label>
            <br />
            <select name="" id="signUpJob" v-model="signUpJob">
              <option value="" disabled>직업 선택하기</option>
              <option
                :value="data"
                style="width: 100%"
                v-for="data in ['공무원', '변호사', '의사', '회사원', '엔지니어', '개발자', '교수', '간호사']"
                :key="data"
              >
                {{ data }}
              </option>
            </select>
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
        <button class="px-4 py-2 mt-4" id="signUpCk">회원가입</button>
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
const signUpJob = ref(null);

const authStore = useAuthStore();

const resetData = () => {
  signUpDom.value = null;
  signUpId.value = null;
  signUpPw.value = null;
  signUpPwCk.value = null;
  signUpName.value = null;
  signUpAge.value = null;
  signUpEmail.value = null;
  signUpMoney.value = null;
  signUpSalary.value = null;
  signUpJob.value = null;
};

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
    job: signUpJob.value,
  };
  const dialog = document.querySelector("#moveSignUpPage");
  dialog.close();
  authStore.signUp(payload);
  resetData();
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    signUpDom.value.close();
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
  overflow-y: scroll;
}

dialog::-webkit-scrollbar {
  width: 10px; /* 스크롤바의 너비 */
}

dialog::-webkit-scrollbar-thumb {
  background: lightgray; /* 스크롤바의 색상 */
  border-radius: 10px;
}

label {
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
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

#signUpCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bold;
  position: sticky;
  bottom: 24px;
  /* margin-top: 24px; */
  width: 100%;
  /* bottom: 24px; */
}

#signUpForm {
  margin: 0 auto;
  padding: 20px 20px 0;
  border-radius: 5px;
}

#closeSignUpDialog {
  border: 0px;
  background-color: transparent;
}

.closeSignUpDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
