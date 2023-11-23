<template>
  <dialog @click="closeModal" ref="depositJoinDom">
    <div v-if="deposit" id="hhh" class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeDepositJoinDialog">
          <font-awesome-icon :icon="['fas', 'xmark']" class="closeDepositJoinDialog" />
        </button>
      </form>
      <!-- <p>{{ deposit }}</p> -->
      <h2 class="text-center">정기예금 가입</h2>
      <form id="depositJoinForm" class="d-flex flex-column gap-3" @submit.prevent="joinDeposit">
        <div>
          <label for="amount">예치금:</label>
          <br />
          <input v-model.trim="depositJoinAmount" type="number" id="amount" name="amount" placeholder="금액을 입력해주세요." required />
        </div>
        <div>
          <label for="months">가입개월:</label>
          <br />
          <!-- <input type="number" id="months" name="months" required /> -->
          <select name="" id="months" v-model="depositJoinPeriod">
            <option :value="0" disabled>기간을 선택하세요</option>
            <option v-for="option in deposit.depositoptions_set" :key="option.id" :value="option.id">{{ option.save_trm }} 개월</option>
          </select>
        </div>
        <button class="px-4 py-2 mt-3" id="depositJoinCk">가입하기</button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";
import { useRoute } from "vue-router";

const authStore = useAuthStore();
const depositJoinDom = ref(null);
const route = useRoute();

const depositJoinAmount = ref("");
const depositJoinPeriod = ref(0);

const props = defineProps({
  deposit: Object,
});

const resetData = () => {
  depositJoinAmount.value = "";
  depositJoinPeriod.value = 0;
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    depositJoinDom.value.close();
    resetData();
  }
};

const joinDeposit = () => {
  console.log(depositJoinPeriod.value);
  console.log(typeof depositJoinPeriod.value);
  console.log(depositJoinAmount.value);
  console.log(typeof depositJoinAmount.value);
  axios({
    method: "post",
    url: `${authStore.API_URL}/banking/deposits/${route.params.depositId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
    data: {
      option_id: depositJoinPeriod.value,
      amount: depositJoinAmount.value,
    },
  })
    .then((res) => {
      console.log(res.data);
      authStore.user.financial_products = res.data.user.financial_products;
      const dialog = document.querySelector("#moveJoinPage");
      dialog.close();
      resetData();
    })
    .catch((err) => {
      console.log(err);
    });
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
  height: 500px;
  width: 500px;
}

label {
  /* display: block; */
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 4px;
  /* box-sizing: border-box; */
}

.move {
  right: 10px;
}

#hhh {
  height: 100%;
}

#depositJoinForm {
  margin: 0 auto;
  padding: 20px;
  border-radius: 5px;
}

#closeDepositJoinDialog {
  border: 0px;
  background-color: transparent;
}

.closeDepositJoinDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}

#depositJoinCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bold;
}
</style>
