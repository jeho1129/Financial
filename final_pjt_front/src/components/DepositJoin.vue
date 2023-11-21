<template>
  <dialog @click="closeModal" ref="depositJoinDom">
    <div id="hhh" class="position-relative p-4">
      <form method="dialog" class="position-absolute move">
        <button value="close">❌</button>
      </form>
      <h2 class="text-center">정기예금 가입</h2>
      <form id="depositForm" class="d-flex flex-column gap-3">
        <div>
          <label for="amount">예치금:</label>
          <br />
          <input v-model.trim="DepositJoinAmount" type="number" id="amount" name="amount" required />
        </div>

        <div>
          <label for="months">가입개월:</label>
          <br />
          <!-- <input type="number" id="months" name="months" required /> -->
          <select name="" id="months" v-model.trim="DepositJoinPeriod">
            <option :value="0">기간을 선택하세요</option>
            <option v-for="option in depositOption" :key="option.id" value="option.save_trm">{{ option.save_trm }} 개월</option>
          </select>
        </div>
        <button class="btn btn-primary">가입하기</button>
      </form>
    </div>
  </dialog>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
const depositJoinDom = ref(null);

const DepositJoinAmount = ref(0);
const DepositJoinPeriod = ref(0);

const props = defineProps({
  deposit: Object,
});

const depositOption = props.deposit.depositoptions_set;

const closeModal = (e) => {
  if (e.target.nodeName === "DIALOG") {
    depositJoinDom.value.close();
  }
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

#depositForm {
  margin: 0 auto;
  padding: 20px;
  border-radius: 5px;
}

label {
  /* display: block; */
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="number"] {
  width: 100%;
  padding: 10px;
  border: 1px solid lightgray;
  border-radius: 4px;
  /* box-sizing: border-box; */
}

/* input[type="submit"] {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
} */

/* input[type="submit"]:hover {
  background-color: #45a049;
} */
</style>
