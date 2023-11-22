<template>
  <div>
    <Carousel />
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
            class="popularProduct"
            style="cursor: pointer"
            @click="moveDepositDetail(base.fin_prdt_cd)"
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
            class="popularProduct"
            style="cursor: pointer"
            @click="moveSavingDetail(base.fin_prdt_cd)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Carousel from "../components/Carousel.vue";
import CardProduct from "../components/CardProduct.vue";
import { RouterLink, RouterView, useRouter } from "vue-router";
import { onMounted } from "vue";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";

const depositStore = useDepositStore();
const savingStore = useSavingStore();
const router = useRouter();

onMounted(() => {
  if (!depositStore.deposit.length) {
    depositStore.callDeposit();
  }
  if (!savingStore.saving.length) {
    savingStore.callSaving();
  }
});

const moveDepositDetail = (id) => {
  router.push({ name: "depositDetail", params: { depositId: id } });
};

const moveSavingDetail = (id) => {
  router.push({ name: "savingDetail", params: { savingId: id } });
};
</script>

<style scoped>
a {
  text-decoration-line: none;
  color: #5fb9a6;
}

.popularProduct {
  border: 1px solid lightgray;
  border-radius: 5px;
}

.popularProduct:hover {
  font-weight: bold;
  transform: scale(1.05);
  color: #5fb9a6;
  transition-duration: 0.3s;
  box-shadow: 1px 1px 20px #ddd;
}
</style>
