<template>
  <div>
    <h1>테스트{{ route.params.savingId }}</h1>
    <div v-if="saving">
      {{ saving }}
    </div>
    <form>
      <button>가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const authStore = useAuthStore();
const savingId = route.params.savingId;
const saving = ref(null);

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/savings/${savingId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      saving.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
});
</script>

<style scoped></style>
