<template>
  <div class="container">
    <div
      v-if="deposit"
      class="d-flex justify-content-between align-items-center my-4"
    >
      <h1 class="mb-0">정기예금 상세</h1>

      <div v-if="authStore.user">
        <form
          v-if="
            authStore.user.financial_products
              .split(', ')
              .includes(deposit.fin_prdt_cd)
          "
          @submit.prevent="joinDeposit"
        >
          <button>가입취소</button>
        </form>
        <form v-else @submit.prevent="joinDeposit">
          <button>가입하기</button>
        </form>
      </div>
    </div>

    <table v-if="deposit">
      <tbody>
        <tr>
          <th>금융회사명</th>
          <td>{{ deposit.kor_co_nm }}</td>
        </tr>
        <tr>
          <th>상품명</th>
          <td>{{ deposit.fin_prdt_nm }}</td>
        </tr>
        <tr>
          <th>가입제한</th>
          <td>{{ deposit.join_deny }}</td>
        </tr>
        <tr>
          <th>가입 방법</th>
          <td>{{ deposit.join_way }}</td>
        </tr>
        <tr>
          <th>우대조건</th>
          <td>
            <p v-for="data in deposit.spcl_cnd.split('\n')" :key="data">
              {{ data }}
            </p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";

const route = useRoute();
const authStore = useAuthStore();
const depositId = route.params.depositId;
const deposit = ref(null);

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/deposits/${depositId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
      // "Content-Type": "text/plain",
    },
  })
    .then((res) => {
      deposit.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
});

const joinDeposit = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/banking/deposits/${deposit.value.fin_prdt_cd}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
/* .table {
  border-color: white;
} */
th,
td {
  padding: 20px;
}
</style>
