<template>
  <div class="defaultMyProfile p-4">
    <div>
      <div class="d-flex justify-content-between">
        <h4>기본 정보</h4>
        <button @click="someEvent" class="p-2" id="moveProfileEdit">수정하기</button>
        <!-- <button v-else @click="dddd" class="p-2" id="moveProfileEdit">수정하기</button> -->
      </div>
      <div class="d-flex align-items-center gap-4">
        <img src="../assets/profile.jpg" alt="" />
        <p class="m-0">{{ authStore.user.name || "admin" }}</p>
      </div>
      <hr />
      <table>
        <tbody>
          <tr>
            <th>아이디</th>
            <td>{{ authStore.user.username }}</td>
          </tr>
          <tr>
            <th>이메일</th>
            <td>{{ authStore.user.email || "이메일을 설정해주세요" }}</td>
          </tr>
          <tr>
            <th>비밀번호</th>
            <td>
              <button id="changePassword" @click="changePassword">비밀번호 변경</button>
            </td>
          </tr>
          <tr>
            <th>나이</th>
            <td>{{ authStore.user.age }}</td>
          </tr>
          <tr>
            <th>직업</th>
            <td>{{ authStore.user.job }}</td>
          </tr>
          <tr>
            <th>자산</th>
            <td>{{ authStore.user.asset || "금액을 설정해주세요" }}</td>
          </tr>
          <tr>
            <th>연봉</th>
            <td>{{ authStore.user.salary || "금액을 설정해주세요" }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <ChangePassWord id="moveChangePassWord" />
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import ChangePassWord from "./ChangePassWord.vue";

const authStore = useAuthStore();

const emit = defineEmits("someEvent");
const someEvent = () => {
  emit("someEvent");
};

const changePassword = () => {
  const dialog = document.querySelector("#moveChangePassWord");
  dialog.showModal();
};
</script>

<style scoped>
.defaultMyProfile {
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
  color: white;
  font-weight: bolder;
  border-radius: 5px;
}

#moveProfileEdit:hover {
  filter: brightness(0.9);
}

td {
  padding: 10px;
}

#changePassword {
  background-color: #5fb9a6;
  color: white;
  font-weight: bolder;
  border: 0px;
  border-radius: 5px;
  border: 1px solid lightgray;
}
</style>
