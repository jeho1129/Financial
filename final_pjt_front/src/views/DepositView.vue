<template>
  <div class="mt-5 container" id="depositMain">
    <div class="d-flex gap-2 align-items-center" id="depositHead">
      <RouterLink id="fromDeposit" :to="{ name: 'deposit' }"
        >정기예금</RouterLink
      >
      |
      <RouterLink :to="{ name: 'saving' }">정기적금</RouterLink>
    </div>
    <div class="d-flex justify-content-between align-items-center">
      <p>전체 {{ depositStore.deposit.length }} 건</p>
      <form @submit.prevent="changeDeposit">
        <select v-model="category">
          <option value="all">은행전체</option>
          <option
            v-for="category in depositStore.categoryBank"
            :key="category"
            :value="category"
          >
            {{ category }}
          </option>
        </select>
        <select v-model="period">
          <option value="all">예치기간전체</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
        <button class="px-4 py-2">검색</button>
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
import { RouterLink } from "vue-router";
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
  /* width: 100%; */
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

#fromDeposit {
  color: #5fb9a6;
}

a {
  text-decoration-line: none;
  color: black;
}
</style>
