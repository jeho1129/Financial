<template>
  <div>
    <Carousel style="z-index: -999" />
    <div
      v-if="depositStore.deposit.length"
      class="container mt-5 d-flex flex-column gap-5"
    >
      <div>
        <div class="d-flex justify-content-between align-items-center">
          <h3>인기 예금</h3>
          <RouterLink to="/deposit">더보기</RouterLink>
        </div>
        <div id="cardArray" class="d-flex justify-content-center gap-2">
          <CardProduct
            v-for="base in depositStore.popularDeposits"
            :key="base.fin_prdt_cd"
            :base="base"
          />
        </div>
      </div>
      <div>
        <div class="d-flex justify-content-between align-items-center">
          <h3>인기 적금</h3>
          <RouterLink to="/saving">더보기</RouterLink>
        </div>
        <div id="cardArray" class="d-flex justify-content-center gap-2">
          <CardProduct
            v-for="base in savingStore.popularSaving"
            :key="base.fin_prdt_cd"
            :base="base"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Carousel from "../components/Carousel.vue";
import CardProduct from "../components/CardProduct.vue";
import { RouterLink, RouterView } from "vue-router";
import { onMounted } from "vue";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";

const depositStore = useDepositStore();
const savingStore = useSavingStore();

onMounted(() => {
  if (!depositStore.deposit.length) {
    depositStore.callDeposit();
  }
  if (!savingStore.saving.length) {
    savingStore.callSaving();
  }
});
</script>

<style scoped>
a {
  text-decoration-line: none;
  color: #5fb9a6;
}
</style>
