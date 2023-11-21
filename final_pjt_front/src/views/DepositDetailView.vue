<template>
  <div class="container">
    <div v-if="deposit" class="d-flex justify-content-between align-items-center my-4">
      <h1 class="mb-0">정기예금 상세</h1>
      <div v-if="authStore.user">
        <div>
          <!-- <form @submit.prevent="joinDeposit"> -->
          <button @click="Join">가입하기</button>
          <!-- .includes(deposit.fin_prdt_cd) -->
          <!-- <button v-else>가입취소</button> -->
          <!-- </form> -->
        </div>
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
    <h1>예금 계산기</h1>
    <form v-if="deposit" @submit.prevent="calculate(amount, rate, period, method)">
      <input type="number" v-model="amount" />
      <select v-model="period" @change="changeRate(period)">
        <option :value="0">기간을 선택하세요</option>
        <option v-for="option in deposit.depositoptions_set" :key="option.id" :value="option.save_trm">{{ option.save_trm }} 개월</option>
      </select>
      <input :value="rate" readonly />
      <button>계산</button>
    </form>
    <p>{{ result }}</p>
    <DepositJoin id="moveJoinPage" :deposit="deposit" />
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import DepositJoin from "../components/DepositJoin.vue";
// period ? deposit.depositoptions_set.find((item) => item.save_trm == period).intr_rate2 : 0
const route = useRoute();
const authStore = useAuthStore();
const depositId = route.params.depositId;
const deposit = ref(null);

const amount = ref(0);
const period = ref(0);
const rate = ref("-");
const method = ref("");
const result = ref(0);

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
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
});
// v-if="!(deposit.fin_prdt_cd in authStore.user.financial_products)"
const joinDeposit = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/banking/deposits/${deposit.value.fin_prdt_cd}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data.message);
      if (res.data.message === "Product added successfully") {
        if (!authStore.user.financial_products) {
          authStore.user.financial_products = { [deposit.value.fin_prdt_cd]: deposit.value };
        } else if (!(deposit.value.fin_prdt_cd in authStore.user.financial_products)) {
          authStore.user.financial_products[deposit.value.fin_prdt_cd] = deposit.value;
        }
      } else if (res.data.message === "가입이 취소되었습니다.") {
        delete authStore.user.financial_products[deposit.value.fin_prdt_cd];
      }
    })
    .catch((err) => {
      console.log(err);
    });
};

const changeRate = (period) => {
  if (period) {
    rate.value = deposit.value.depositoptions_set.find((item) => item.save_trm == period).intr_rate2;
    method.value = deposit.value.depositoptions_set.find((item) => item.save_trm == period).intr_rate_type_nm;
  } else {
    rate.value = "-";
    method.value = "";
  }
};

const Join = () => {
  const dialog = document.querySelector("#moveJoinPage");
  dialog.showModal();
};

function calculate(principal, rate, time, method) {
  rate /= 100;
  console.log(method);
  if (method === "단리") {
    // 예금액 * 이자율 * 기간
    result.value = (principal + (principal * rate * time) / 12).toFixed();
  } else if (method === "복리") {
    // 예금액 * (1 + 이자율) ^ 기간
    result.value = principal * Math.pow(1 + rate, time / 12).toFixed();
  } else {
    result.value = 0;
  }
}
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
