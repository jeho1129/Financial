<template>
  <div>
    <h1>환율 계산기</h1>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted } from "vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

// onMounted(() => {
//   axios({
//     method: "get",
//     url: `${authStore.API_URL}/banking/exchanges/`,
//     headers: {
//       Authorization: `Token ${authStore.token}`,
//     },
//   })
//     .then((res) => {
//       console.log(res);
//     })
//     .catch((err) => {
//       console.log(err);
//     });
// });
</script>

<style scoped></style>
