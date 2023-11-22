<template>
  <div class="container my-4" v-if="authStore.user">
    <div class="d-flex justify-content-center gap-4 my-4">
      <RouterLink :to="{ name: 'myProfile' }" id="fromMyProfile" class="py-2">기본 정보</RouterLink>
      <!-- <RouterLink :to="{ name: 'checkProduct' }" id="toJoinProduct" class="py-2">가입 상품 확인</RouterLink> -->
      <p id="toRecommend" class="m-0 py-2">상품 추천 받기</p>
    </div>
    <!-- <h1 class="text-center">{{ authStore.user.username }} 님의 프로필 페이지</h1> -->
    <div class="d-flex flex-column gap-3">
      <ProfileShow v-if="!ck" @some-event="ck = !ck" />
      <ProfileEdit v-if="ck" @edit-profile="ck = !ck" />
      <CkJoinProduct />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import ProfileShow from "../components/profileShow.vue";
import ProfileEdit from "../components/ProfileEdit.vue";
import CkJoinProduct from "../components/CkJoinProduct.vue";
import { ref } from "vue";

const authStore = useAuthStore();

const ck = ref(0);
</script>

<style scoped>
.container {
  width: 700px;
}

p {
  cursor: pointer;
}

a {
  text-decoration-line: none;
  color: black;
}

#fromMyProfile {
  width: 130px;
  color: #5fb9a6;
  border: 2px solid #5fb9a6;
  font-weight: bold;
  border-radius: 10px;
  text-align: center;
}

#toJoinProduct,
#toRecommend {
  width: 130px;
  color: #333;
  border: 1px solid lightgray;
  font-weight: bold;
  border-radius: 10px;
  text-align: center;
}
</style>
