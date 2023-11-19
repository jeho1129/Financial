<template>
  <div class="d-flex gap-3">
    <div>
      <h4>정기예금</h4>
      <p>검색 조건을 입력하세요</p>
      <hr />
      <form @submit.prevent="changeDeposit" class="d-flex flex-column gap-4">
        <div>
          <label for="">은행을 선택하세요</label>
          <br />
          <select v-model="category">
            <option value="all">전체</option>
            <option
              v-for="category in depositStore.categoryBank"
              :key="category"
              :value="category"
            >
              {{ category }}
            </option>
          </select>
        </div>
        <div>
          <label for="">예치기간</label>
          <br />
          <select v-model="period">
            <option value="all">전체상품</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
        </div>
        <button class="px-4 py-2">확인</button>
      </form>
    </div>
    <table class="table text-center">
      <thead>
        <tr class="table-success">
          <th scope="col">금융회사명</th>
          <th scope="col">상품명</th>
          <th scope="'col'">6개월</th>
          <th scope="'col'">12개월</th>
          <th scope="'col'">24개월</th>
          <th scope="'col'">36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="base in deposit" :key="base.id">
          <td>{{ base.kor_co_nm }}</td>
          <td>{{ base.fin_prdt_nm }}</td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 6;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 12;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 24;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 36;
              })?.intr_rate2 ?? "-"
            }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useDepositStore } from "../stores/deposit";

const depositStore = useDepositStore();

const category = ref("all");
const period = ref("all");
const deposit = ref(depositStore.deposit);

onMounted(() => {
  if (!depositStore.deposit.length) {
    depositStore.callDeposit();
  }
});

const changeDeposit = () => {
  if (period.value === "all" && category.value === "all") {
    deposit.value = depositStore.deposit;
  } else {
    deposit.value = depositStore.searchDeposits(period.value, category.value);
    // console.log(depositStore.searchDeposits(period.value, category.value));
  }
};
</script>

<style scoped>
select {
  width: 200px;
  border: 1px solid #5fb9a6;
  border-radius: 5px;
  padding: 10px;
}

select:focus {
  outline: none;
}

button {
  background-color: #5fb9a6;
  border: 0px;
  border-radius: 5px;
}

button:hover {
  filter: brightness(0.9);
}
</style>
