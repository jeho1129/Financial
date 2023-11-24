<template>
  <div class="container my-4" v-if="authStore.user">
    <div class="d-flex justify-content-center gap-4 my-4">
      <RouterLink :to="{ name: 'myProfile' }" id="toMyProfile" class="py-2">기본 정보</RouterLink>
      <RouterLink :to="{ name: 'recommendProduct' }" id="toMyProfile" class="m-0 py-2">상품 추천 받기 (선호도)</RouterLink>
      <RouterLink :to="{ name: 'recommendProductInfo' }" id="fromRecommend" class="py-2">상품 추천 받기 (유저 정보)</RouterLink>
    </div>
    <div class="d-flex flex-column gap-3">
      <RecommendProductInfo />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import { RouterLink, RouterView } from "vue-router";
import RecommendProductInfo from "../components/RecommendProductInfo.vue";
import { ref } from "vue";

const authStore = useAuthStore();
// const rou
</script>

<style scoped>
.container {
  width: 700px;
}

a {
  text-decoration-line: none;
  color: black;
}

#fromRecommend {
  width: 200px;
  color: #5fb9a6;
  border: 2px solid #5fb9a6;
  font-weight: bold;
  border-radius: 10px;
  text-align: center;
}

#toMyProfile {
  width: 200px;
  color: #333;
  border: 1px solid lightgray;
  font-weight: bold;
  border-radius: 10px;
  text-align: center;
}
</style>
