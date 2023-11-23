<template>
  <dialog @click="closeModal" ref="exchangeRateDom">
    <div v-if="exchangeData.length" id="hhh" class="position-relative p-5">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeExchangeRate"><font-awesome-icon :icon="['fas', 'xmark']" class="closeExchangeRate" /></button>
      </form>
      <div style="text-align: center">
        <img src="../assets/money.png" alt="" style="width: 30%" />
      </div>
      <h2 class="text-center mb-5">환율계산기</h2>
      <div class="d-flex flex-column gap-3">
        <div class="d-flex" id="exchangeRatePrev">
          <select @click="calculateExchange" id="exchangeRatePrevUnit" v-model="exchangeRatePrevUnit">
            <option
              v-for="unit in exchangeData.map((item) => {
                return item.cur_unit;
              })"
              :key="unit"
              :value="unit"
            >
              {{ unit }}
            </option>
          </select>
          <input v-model.trim="exchangeRatePrevMoney" type="number" style="width: 100%" id="exchangeRatePrevMoney" @input="calculateExchange" />
        </div>
        <div class="d-flex my-2 justify-content-between">
          <button @click="changeUnit" class="px-4 py-2" id="exChange">
            <font-awesome-icon :icon="['fas', 'arrow-right-arrow-left']" />
          </button>
          <span> {{ exchangeRatePrevMoney || 0 }}{{ exchangeRatePrevUnit }} - {{ exchangeRateNextMoney || 0 }}{{ exchangeRateNextUnit }} </span>
        </div>
        <div class="d-flex" id="exchangeRateNext">
          <select @click="calculateExchange" id="exchangeRateNextUnit" v-model="exchangeRateNextUnit">
            <option
              v-for="unit in exchangeData.map((item) => {
                return item.cur_unit;
              })"
              :key="unit"
              :value="unit"
            >
              {{ unit }}
            </option>
          </select>
          <input v-model.trim="exchangeRateNextMoney" type="number" style="width: 100%" id="exchangeRateNextMoney" readonly />
        </div>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import axios from "axios";
import { onMounted, onUpdated, ref, watch } from "vue";
import { useAuthStore } from "../stores/auth";
import { computed } from "@vue/reactivity";

const authStore = useAuthStore();

const exchangeRateDom = ref(null);

const exchangeRatePrevMoney = ref(0);
const exchangeRateNextMoney = ref(0);
const exchangeRatePrevUnit = ref("KRW");
const exchangeRateNextUnit = ref("USD");

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    // console.log(exchangeRateDom);
    exchangeRateDom.value.close();
  }
};

const props = defineProps({
  exchangeData: Array,
});

const calculateExchange = () => {
  // 선택된 통화에 해당하는 환율 찾기
  const fromRate = props.exchangeData.find((rate) => rate.cur_unit === exchangeRatePrevUnit.value);
  const toRate = props.exchangeData.find((rate) => rate.cur_unit === exchangeRateNextUnit.value);

  // 환율 계산
  exchangeRateNextMoney.value = (exchangeRatePrevMoney.value / toRate.deal_bas_r.replace(",", "")) * fromRate.deal_bas_r.replace(",", "");
};

const changeUnit = () => {
  [exchangeRatePrevUnit.value, exchangeRateNextUnit.value] = [exchangeRateNextUnit.value, exchangeRatePrevUnit.value];
  calculateExchange();
};
</script>

<style scoped>
dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.8);
}
dialog {
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  border: 0;
  border-radius: 10px;
  padding: 0;
  background-color: whitesmoke;
  /* height: 500px; */
  width: 500px;
}

#exChange {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

#exChange:hover {
  filter: brightness(0.9);
}

.move {
  right: 20px;
  top: 20px;
}

#hhh {
  height: 100%;
}

#moveSignUp {
  cursor: pointer;
  font-weight: bold;
}

#exchangeRatePrev,
#exchangeRateNext {
  padding: 10px;
  background-color: white;
  border-radius: 10px;
}

select:focus,
input:focus {
  outline: none;
}

input {
  text-align: right;
}

#exchangeRatePrevUnit,
#exchangeRatePrevMoney,
#exchangeRateNextUnit,
#exchangeRateNextMoney {
  border: 0px;
}

#closeExchangeRate {
  border: 0px;
  background-color: transparent;
}

.closeExchangeRate {
  width: 30px;
  height: 30px;
  color: lightgray;
}
</style>
