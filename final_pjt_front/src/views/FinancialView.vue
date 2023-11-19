<template>
  <div v-if="depositStore.deposit" class="container">
    <h1>금융상품 비교</h1>
    <div class="d-flex gap-2 my-4">
      <span @click="ck = !ck" :class="{ green: !ck }">정기예금</span>
      |
      <span @click="ck = !ck" :class="{ green: ck }">정기적금</span>
    </div>
    <Deposit v-if="!ck" />
    <Saving v-if="ck" />
  </div>
</template>

<script setup>
import { ref } from "vue";
import Deposit from "../components/Deposit.vue";
import Saving from "../components/Saving.vue";
import { useDepositStore } from "../stores/deposit";

const depositStore = useDepositStore();

const ck = ref(0);
</script>

<style scoped>
.green {
  color: #5fb9a6;
}

span {
  cursor: pointer;
}
</style>
