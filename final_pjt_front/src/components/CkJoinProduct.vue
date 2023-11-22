<template>
  <div class="defaultMyProfile p-4">
    <h4 style="height: 32px">가입 상품</h4>
    <div class="d-flex justify-content-between"></div>
    <hr />
    <!-- <p>{{ authStore.user.financial_products }}</p> -->
    <!-- <p>{{ Object.keys(authStore.user.financial_products) }}</p> -->
    <div>
      <h4>예금</h4>
      <div v-if="!findDeposit.length"></div>
      <div v-else id="searchProducts">
        <div @click="moveProductDetail(info.fin_prdt_cd)" class="searchProduct" v-for="info in findDeposit">
          <p>{{ info.fin_prdt_nm }}</p>
          <p>{{ info.kor_co_nm }}</p>
        </div>
      </div>
    </div>
    <hr />
    <div>
      <h4>적금</h4>
      <div v-if="!findSaving.length">가입된 상품이 없습니다</div>
      <div v-else id="searchProducts">
        <div @click="moveProductDetail(info.fin_prdt_cd)" class="searchProduct" v-for="info in findSaving">
          <p>{{ info.fin_prdt_nm }}</p>
          <p>{{ info.kor_co_nm }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";

const authStore = useAuthStore();
const depositStore = useDepositStore();
const savingStore = useSavingStore();
const router = useRouter();

const findDeposit = depositStore.deposit.filter((item) => Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd));
const findSaving = savingStore.saving.filter((item) => Object.keys(authStore.user.financial_products).includes(item.fin_prdt_cd));

const moveProductDetail = (id) => {
  router.push({ name: "depositDetail", params: { depositId: id } });
};
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

#searchProducts {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

.searchProduct {
  border: 1px solid lightgray;
  border-radius: 5px;
}

.searchProduct:hover {
  font-weight: bold;
  transform: scale(1.05);
  color: #5fb9a6;
  transition-duration: 0.3s;
  box-shadow: 1px 1px 20px #ddd;
}
</style>
