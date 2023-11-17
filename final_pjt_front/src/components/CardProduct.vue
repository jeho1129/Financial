<template>
  <div class="card" style="width: 18rem">
    <!-- {{ base }} -->
    <div class="card-body">
      <h5 class="card-title">{{ base.kor_co_nm }}</h5>
      <h6 class="card-subtitle mb-2 text-body-secondary">{{ base.fin_prdt_nm }}</h6>
      <p class="card-text">#{{ base.join_way }}</p>
      <!-- <a href="#" class="card-link">Card link</a> -->
      <!-- <a href="#" class="card-link">Another link</a> -->
    </div>
  </div>
</template>

<script setup>
defineProps({
  base: Object,
});
</script>

<style scoped></style>
