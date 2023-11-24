<template>
  <div class="defaultMyProfile p-4">
    <h4>상품 추천 받기</h4>
    <div style="font-weight: bolder; text-align: center" class="d-flex flex-column gap-2 m-4 text-secondary">
      <p class="m-0">{{ authStore.user.name || "admin" }}님만을 위해 준비한 특별한 추천</p>
      <p class="m-0">당신의 회원정보를 반영한 최적의 금융 상품을 찾아봤어요.</p>
    </div>

    <div v-if="ageDeposit.length">
      <div v-for="deposit in ageDeposit" :key="deposit">
        <div class="searchProduct">
          (정기예금){{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).kor_co_nm }} -
          <span @click="moveDeposit(deposit)">{{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).fin_prdt_nm }}</span>
        </div>
      </div>
      <div v-for="saving in ageSaving" :key="saving">
        <div class="searchProduct">
          (정기적금){{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).kor_co_nm }} -
          <span @click="moveSaving(saving)">{{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).fin_prdt_nm }}</span>
        </div>
      </div>
    </div>
    <div v-if="jobDeposit.length">
      <div v-for="deposit in jobDeposit" :key="deposit">
        <div class="searchProduct">
          (정기예금){{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).kor_co_nm }} -
          <span @click="moveDeposit(deposit)">{{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).fin_prdt_nm }}</span>
        </div>
      </div>
      <div v-for="saving in jobSaving" :key="saving">
        <div class="searchProduct">
          (정기적금){{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).kor_co_nm }} -
          <span @click="moveSaving(saving)">{{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).fin_prdt_nm }}</span>
        </div>
      </div>
    </div>
    <div v-if="assetDeposit.length">
      <div v-for="deposit in assetDeposit" :key="deposit">
        <div class="searchProduct">
          (정기예금){{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).kor_co_nm }} -
          <span @click="moveDeposit(deposit)">{{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).fin_prdt_nm }}</span>
        </div>
      </div>
      <div v-for="saving in assetSaving" :key="saving">
        <div class="searchProduct">
          (정기적금){{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).kor_co_nm }} -
          <span @click="moveSaving(saving)">{{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).fin_prdt_nm }}</span>
        </div>
      </div>
    </div>
    <div v-if="salaryDeposit.length">
      <div v-for="deposit in salaryDeposit" :key="deposit">
        <div class="searchProduct">
          (정기예금){{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).kor_co_nm }} -
          <span @click="moveDeposit(deposit)">{{ depositStore.deposit.find((item) => item.fin_prdt_cd === deposit).fin_prdt_nm }}</span>
        </div>
      </div>
      <div v-for="saving in salarySaving" :key="saving">
        <div class="searchProduct">
          (정기적금){{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).kor_co_nm }} -
          <span @click="moveSaving(saving)">{{ savingStore.saving.find((item) => item.fin_prdt_cd === saving).fin_prdt_nm }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useDepositStore } from "../stores/deposit";
import { useSavingStore } from "../stores/saving";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const depositStore = useDepositStore();
const savingStore = useSavingStore();
const router = useRouter();

const ageDeposit = ref([]);
const ageSaving = ref([]);
const jobDeposit = ref([]);
const jobSaving = ref([]);
const assetDeposit = ref([]);
const assetSaving = ref([]);
const salaryDeposit = ref([]);
const salarySaving = ref([]);

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/recommends/sort/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      ageDeposit.value = res.data.age_deposit_products;
      ageSaving.value = res.data.age_saving_products;
      jobDeposit.value = res.data.job_deposit_products;
      jobSaving.value = res.data.job_saving_products;
      assetDeposit.value = res.data.asset_deposit_products;
      assetSaving.value = res.data.asset_saving_products;
      salaryDeposit.value = res.data.salary_deposit_products;
      salarySaving.value = res.data.salary_saving_products;
    })

    .catch((err) => {
      console.log(err);
    });
});

const moveDeposit = (id) => {
  router.push({ name: "depositDetail", params: { depositId: id } });
};

const moveSaving = (id) => {
  router.push({ name: "savingDetail", params: { savingId: id } });
};
</script>

<style scoped>
.defaultMyProfile {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

#moveProfileEdit {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

#moveProfileEdit:hover {
  filter: brightness(0.9);
}

span {
  color: #5fb9a6;
  font-weight: bold;
  cursor: pointer;
}

.searchProduct {
  /* border: 1px solid lightgray; */
  /* border-radius: 5px; */
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
