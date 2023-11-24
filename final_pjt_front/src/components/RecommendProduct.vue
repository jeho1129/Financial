<template>
  <div class="defaultMyProfile p-4">
    <h4>상품 추천 받기</h4>
    <div style="font-weight: bolder; text-align: center" class="d-flex flex-column gap-2 m-4 text-secondary">
      <p class="m-0">{{ authStore.user.name || "admin" }}님만을 위해 준비한 특별한 추천</p>
      <p class="m-0">당신의 선호도를 반영한 최적의 금융 상품을 찾아봤어요.</p>
    </div>
    <div v-if="recommendDeposit.length">
      <div v-for="deposit in recommendDeposit" :key="deposit">
        <div class="searchProduct">
          (정기예금){{ depositStore.deposit[deposit - 1].kor_co_nm }} -
          <span @click="moveDeposit(depositStore.deposit[deposit - 1].fin_prdt_cd)">{{ depositStore.deposit[deposit - 1].fin_prdt_nm }}</span>
        </div>
      </div>
      <div v-for="saving in recommendSaving" :key="saving">
        <div class="searchProduct">
          (정기적금){{ savingStore.saving[saving - 1].kor_co_nm }} -
          <span @click="moveSaving(savingStore.saving[saving - 1].fin_prdt_cd)">{{ savingStore.saving[saving - 1].fin_prdt_nm }}</span>
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

const recommendDeposit = ref([]);
const recommendSaving = ref([]);

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/deposits/recommends/load/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      axios({
        method: "get",
        url: `${authStore.API_URL}/banking/deposits/recommends/${authStore.user.id}/5/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
      }).then((res) => {
        recommendDeposit.value = res.data.recommended_items;
      });
    })

    .catch((err) => {
      console.log(err);
    });

  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/savings/recommends/load/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      axios({
        method: "get",
        url: `${authStore.API_URL}/banking/savings/recommends/${authStore.user.id}/5/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
      }).then((res) => {
        recommendSaving.value = res.data.recommended_items;
      });
    })

    .catch((err) => {
      console.log(err);
    });

  // axios({
  //   method: "get",
  //   url: `${authStore.API_URL}/banking/recommends/sort/`,
  //   headers: {
  //     Authorization: `Token ${authStore.token}`,
  //   },
  // })
  //   .then((res) => {
  //     console.log(res);
  //   })

  //   .catch((err) => {
  //     console.log(err);
  //   });
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
