<template>
  <div class="defaultMyProfile p-4">
    <h4 style="height: 32px">가입 상품</h4>
    <hr />
    <div v-if="!findDeposit.length && !findSaving.length">
      가입된 상품이 없습니다
    </div>
    <div v-else>
      <template v-if="findDeposit.length">
        <div class="searchProduct" v-for="info in findDeposit" :key="info.id">
          (정기예금) {{ info.kor_co_nm }} -
          <span @click="moveDeposit(info.fin_prdt_cd)">{{
            info.fin_prdt_nm
          }}</span>
        </div>
      </template>
      <template v-if="findSaving.length">
        <div class="searchProduct" v-for="info in findSaving">
          (정기적금) {{ info.kor_co_nm }} -
          <span @click="moveSaving(info.fin_prdt_cd)">{{
            info.fin_prdt_nm
          }}</span>
        </div>
      </template>
    </div>
    <div
      v-if="
        authStore.user.financial_products &&
        Object.keys(authStore.user.financial_products).length
      "
    >
      <hr />
      <Chart :find-deposit="findDeposit" :find-saving="findSaving" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";
import { onMounted, ref } from "vue";
import Chart from "./Chart.vue";

const authStore = useAuthStore();
const depositStore = useDepositStore();
const savingStore = useSavingStore();
const router = useRouter();

const findDeposit = ref([]);
const findSaving = ref([]);
const totalProduct = ref([]);

const moveDeposit = (id) => {
  router.push({ name: "depositDetail", params: { depositId: id } });
};

const moveSaving = (id) => {
  router.push({ name: "savingDetail", params: { savingId: id } });
};

onMounted(() => {
  if (
    authStore.user.financial_products &&
    Object.keys(authStore.user.financial_products)
  ) {
    totalProduct.value = authStore.user.financial_products;
    findDeposit.value = depositStore.deposit.filter((item) =>
      Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd)
    );
    findSaving.value = savingStore.saving.filter((item) =>
      Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd)
    );
  }
});
</script>

<style scoped>
.defaultMyProfile {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

img {
  width: 60px;
  border-radius: 50%;
}

#moveProfileEdit {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

#moveProfileEdit:hover {
  filter: brightness(0.9);
}

td {
  padding: 10px;
}

.searchProduct {
  /* border: 1px solid lightgray; */
  /* border-radius: 5px; */
  padding-top: 10px;
  padding-bottom: 10px;
}

span {
  color: #5fb9a6;
  font-weight: bold;
  cursor: pointer;
}
</style>
