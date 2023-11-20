<template>
  <div class="container">
    <h1 class="text-center">{{ authStore.user.username }} 님의 프로필 페이지</h1>
    <div id="editProfile">
      <div>
        <RouterLink :to="{ name: 'myProfile' }">기본 정보 수정</RouterLink>
        <RouterLink :to="{ name: 'myProfile' }" style="color: #5fb9a6">가입 상품 확인</RouterLink>
        <p>상품 추천 받기</p>
      </div>
      <div>
        <p v-for="product in authStore.user.financial_products.split(', ')" :key="product">
          {{ product }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";

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
