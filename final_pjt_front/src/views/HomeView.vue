<template>
  <div>
    <Carousel />

    <div class="container">
      <div class="d-flex justify-content-between">
        <h3>인기 예금</h3>
        <RouterLink to="/financial">더보기</RouterLink>
        <!-- <p class="d-flex pb-0"></p> -->
      </div>
      <div id="cardArray" class="d-flex justify-content-center gap-2">
        <CardProduct v-for="base in depositStore.popularDeposits" :key="base.fin_prdt_cd" :base="base" />
      </div>
      <div class="d-flex justify-content-between">
        <h3>인기 적금</h3>
        <RouterLink to="/financial">더보기</RouterLink>
        <!-- <p class="d-flex pb-0"></p> -->
      </div>
      <div id="cardArray" class="d-flex justify-content-center gap-2">
        <CardProduct v-for="base in depositStore.popularDeposits" :key="base.fin_prdt_cd" :base="base" />
      </div>
    </div>
  </div>
</template>

<script setup>
import Carousel from "../components/Carousel.vue";
import { useDepositStore } from "../stores/deposit";
import CardProduct from "../components/CardProduct.vue";
import { RouterLink, RouterView } from "vue-router";

const depositStore = useDepositStore();
</script>

<style scoped>
a {
  text-decoration-line: none;
}
</style>
