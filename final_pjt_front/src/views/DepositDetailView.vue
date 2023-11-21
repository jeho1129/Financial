<template>
  <div class="container my-4">
    <div v-if="deposit" class="d-flex flex-column gap-3">
      <div class="depositDetailInfo p-4">
        <h3>{{ deposit.fin_prdt_nm }}</h3>
        <p>{{ deposit.kor_co_nm }}</p>
        <p>#{{ deposit.join_way }}</p>
        <div class="d-flex gap-4">
          <div>
            <p>최고</p>
            <!-- <p>{{ deposit.depositoptions_set }}</p> -->
            <p v-for="option in deposit.depositoptions_set" :key="option.id">
              연 {{ option.intr_rate2 }}%
            </p>
          </div>
          <div>
            <p>기본</p>
            <p v-for="option in deposit.depositoptions_set" :key="option.id">
              연 {{ option.intr_rate ?? option.intr_rate2 }}% ({{
                option.save_trm
              }}개월, 세전)
            </p>
          </div>
        </div>
        <div v-if="authStore.user">
          <button
            v-if="
              !authStore.user.financial_products ||
              !(depositId in authStore.user.financial_products)
            "
            @click="Join"
            class="px-4 py-2 exChange"
          >
            가입하기
          </button>
          <form v-else @submit.prevent="joinDeposit">
            <button class="px-4 py-2 exChange">가입취소</button>
          </form>
        </div>
      </div>
      <div class="depositDetailInfo p-4">
        <h3>이자 계산기</h3>
        <form v-if="deposit" @submit.prevent="1">
          <div>
            <label for="">예치금액</label>
            <br />
            <input type="number" v-model="amount" />
          </div>
          <!-- <p>{{ deposit.depositoptions_set }}</p> -->
          <div class="select d-flex gap-4 justify-content-center">
            <div
              @click="
                calculate(
                  amount,
                  option.intr_rate ?? option.intr_rate2,
                  option.save_trm,
                  option.intr_rate_type_nm
                )
              "
              v-for="option in deposit.depositoptions_set"
              :key="option.id"
            >
              <input
                type="radio"
                v-model="btn"
                :id="`select${option.id}`"
                name="shop"
                :value="option.save_trm"
              /><label
                :for="`select${option.id}`"
                class="py-3 d-flex flex-column gap-2"
              >
                <p class="m-0">
                  {{ option.save_trm }}개월({{ option.intr_rate_type_nm }})
                </p>
                <p class="m-0">
                  기본 {{ option.intr_rate ?? option.intr_rate2 }}%
                </p>
              </label>
            </div>
          </div>
          <div>
            <p class="text-center">
              {{ amount }}원 예금하면 총 세전 이자 {{ result }}원
            </p>
          </div>
        </form>
      </div>
      <div class="depositDetailInfo p-4">
        <h3>상품 정보</h3>
        <div>
          <p>가입 대상</p>
          <p>{{ deposit.join_member }}</p>
        </div>
        <hr />
        <div>
          <p>가입 방법</p>
          <p>{{ deposit.join_way }}</p>
        </div>
        <hr />
        <div>
          <p>우대조건</p>
          <p v-for="data in deposit.spcl_cnd.split('\n')" :key="data">
            {{ data }}
          </p>
        </div>
      </div>
    </div>
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
const result = ref(0);
const btn = ref(0);

onMounted(() => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/deposits/${depositId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
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
      delete authStore.user.financial_products[deposit.value.fin_prdt_cd];
      // if (res.data.message === "Product added successfully") {
      //   if (!authStore.user.financial_products) {
      //     authStore.user.financial_products = {
      //       [deposit.value.fin_prdt_cd]: deposit.value,
      //     };
      //   } else if (
      //     !(deposit.value.fin_prdt_cd in authStore.user.financial_products)
      //   ) {
      //     authStore.user.financial_products[deposit.value.fin_prdt_cd] =
      //       deposit.value;
      //   }
      // } else if (res.data.message === "가입이 취소되었습니다.") {

      // }
    })
    .catch((err) => {
      console.log(err);
    });
};

const Join = () => {
  const dialog = document.querySelector("#moveJoinPage");
  dialog.showModal();
};

function calculate(principal, rate, time, method) {
  rate /= 100;
  // console.log(method);
  if (method === "단리") {
    // 예금액 * 이자율 * 기간
    console.log((principal * rate * time) / 12);
    result.value = ((principal * rate * time) / 12).toFixed();
  } else if (method === "복리") {
    // 예금액 * (1 + 이자율) ^ 기간
    result.value =
      principal * Math.pow(1 + rate, time / 12).toFixed() - principal;
  } else {
    result.value = 0;
  }
}
</script>

<style scoped>
.container {
  width: 700px;
}

.depositDetailInfo {
  background-color: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

.exChange {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  width: 100%;
}

.exChange:hover {
  filter: brightness(0.9);
}

input[type="number"] {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 4px;
}

.select {
  padding: 15px 10px;
}
.select input[type="radio"] {
  display: none;
}
.select input[type="radio"] + label {
  display: inline-block;
  cursor: pointer;
  /* height: 24px; */
  width: 90px;
  border: 1px solid lightgray;
  /* line-height: 24px; */
  text-align: center;
  font-weight: bold;
  font-size: 13px;
  background-color: #fff;
  color: #333;
  border-radius: 10px;
}

.select input[type="radio"]:checked + label {
  /* background-color: #333; */
  border: 2px solid #5fb9a6;
  color: #5fb9a6;
}
</style>
