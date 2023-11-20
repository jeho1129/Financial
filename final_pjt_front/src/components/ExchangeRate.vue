<template>
  <dialog @click="closeModal" ref="exchangeRateDom">
    <div id="hhh" class="position-relative p-5">
      <form method="dialog" class="position-absolute move">
        <button value="close">❌</button>
      </form>
      <div style="text-align: center">
        <img src="../assets/money.png" alt="" style="width: 30%" />
      </div>
      <h2 class="text-center mb-5">환율계산기</h2>
      <div class="d-flex flex-column gap-3">
        <div class="d-flex" id="exchangeRatePrev">
          <select id="exchangeRatePrevUnit" v-model="exchangeRatePrevUnit">
            <option value="KRW">KRW</option>
          </select>
          <input v-model.trim="exchangeRatePrevMoney" type="number" style="width: 100%" id="exchangeRatePrevMoney" />
        </div>
        <div class="d-flex my-2 justify-content-between">
          <button class="px-4 py-2" id="exChange">
            <font-awesome-icon :icon="['fas', 'arrow-right-arrow-left']" />
          </button>
          <span> {{ exchangeRatePrevMoney || 0 }}{{ exchangeRatePrevUnit }} - {{ exchangeRateNextMoney || 0 }}{{ exchangeRateNextUnit }} </span>
        </div>
        <div class="d-flex" id="exchangeRateNext">
          <select id="exchangeRateNextUnit" v-model="exchangeRateNextUnit">
            <option value="USD">USD</option>
          </select>
          <input v-model.trim="exchangeRateNextMoney" type="number" style="width: 100%" id="exchangeRateNextMoney" />
        </div>
      </div>
    </div>
  </dialog>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();

const exchangeRateDom = ref(null);

const exchangeRatePrevMoney = ref(0);
const exchangeRateNextMoney = ref(0);
const exchangeRatePrevUnit = ref("KRW");
const exchangeRateNextUnit = ref("USD");

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    exchangeRateDom.value.close();
  }
};

// onMounted(() => {
//   axios({
//     method: "get",
//     url: `${authStore.API_URL}/banking/exchanges/`,
//     headers: {
//       Authorization: `Token ${authStore.token}`,
//     },
//   })
//     .then((res) => {
//       console.log(res);
//     })
//     .catch((err) => {
//       console.log(err);
//     });
// });
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
  right: 15px;
  top: 15px;
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
</style>
