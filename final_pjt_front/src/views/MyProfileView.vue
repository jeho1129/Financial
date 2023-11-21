<template>
  <div class="container" v-if="authStore.user">
    <h1 class="text-center">{{ authStore.user.username }} 님의 프로필 페이지</h1>
    <div id="editProfile">
      <div class="d-flex flex-column">
        <RouterLink :to="{ name: 'myProfile' }" style="color: #5fb9a6">기본 정보 수정</RouterLink>
        <RouterLink :to="{ name: 'checkProduct' }">가입 상품 확인</RouterLink>
        <p>상품 추천 받기</p>
      </div>
      <div>
        <h3>기본 정보 수정</h3>
        <button @click="ck = !ck">수정하기</button>
        <ProfileShow v-if="!ck" />
        <ProfileEdit v-if="ck" @edit-profile="ck = !ck" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import ProfileShow from "../components/profileShow.vue";
import ProfileEdit from "../components/ProfileEdit.vue";
import { ref } from "vue";

const authStore = useAuthStore();

const ck = ref(0);
</script>

<style scoped>
#editProfile {
  display: grid;
  grid-template-columns: 1fr 4fr;
  grid-gap: 20px;
}

p {
  cursor: pointer;
}

a {
  text-decoration-line: none;
  color: black;
}
</style>
