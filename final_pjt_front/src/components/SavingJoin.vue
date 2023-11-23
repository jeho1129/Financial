<template>
  <dialog @click="closeModal" ref="savingJoinDom">
    <div v-if="saving" id="hhh" class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close" id="closeSavingJoinDialog">
          <font-awesome-icon
            :icon="['fas', 'xmark']"
            class="closeSavingJoinDialog"
          />
        </button>
      </form>
      <!-- <p>{{ deposit }}</p> -->
      <h2 class="text-center">정기적금 가입</h2>
      <form
        id="savingForm"
        class="d-flex flex-column gap-3"
        @submit.prevent="joinSaving"
      >
        <div>
          <label for="amount">예치금:</label>
          <br />
          <input
            v-model.trim="savingJoinAmount"
            type="number"
            id="amount"
            name="amount"
            placeholder="금액을 입력해주세요."
            required
          />
        </div>
        <div>
          <label for="months">가입개월:</label>
          <br />
          <select name="" id="months" v-model="savingJoinPeriod">
            <option :value="0" disabled>기간을 선택하세요</option>
            <option
              v-for="option in saving.savingoptions_set"
              :key="option.id"
              :value="option.id"
            >
              {{ option.save_trm }} 개월
            </option>
          </select>
        </div>
        <button class="px-4 py-2 mt-3" id="savingJoinCk">가입하기</button>
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
const savingJoinDom = ref(null);
const route = useRoute();

const savingJoinAmount = ref("");
const savingJoinPeriod = ref(0);

const props = defineProps({
  saving: Object,
});

const resetData = () => {
  savingJoinAmount.value = "";
  savingJoinPeriod.value = 0;
};

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    savingJoinDom.value.close();
    resetData();
  }
};

const joinSaving = () => {
  axios({
    method: "post",
    url: `${authStore.API_URL}/banking/savings/${route.params.savingId}/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
    data: {
      option_id: savingJoinPeriod.value,
      amount: savingJoinAmount.value,
    },
  })
    .then((res) => {
      authStore.user.financial_products = res.data.user.financial_products;
      const dialog = document.querySelector("#moveJoinSavingPage");
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

.move {
  right: 10px;
}

#hhh {
  height: 100%;
}

#savingForm {
  margin: 0 auto;
  padding: 20px;
  border-radius: 5px;
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

#closeSavingJoinDialog {
  border: 0px;
  background-color: transparent;
}

.closeSavingJoinDialog {
  width: 30px;
  height: 30px;
  color: lightgray;
}

#savingJoinCk {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
  font-weight: bold;
}
</style>
