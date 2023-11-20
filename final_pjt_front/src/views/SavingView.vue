<template>
  <div class="mt-5 container" id="depositMain">
    <div class="d-flex gap-2 align-items-center" id="depositHead">
      <RouterLink class="fs-4" :to="{ name: 'deposit' }">정기예금</RouterLink>
      |
      <RouterLink class="fs-4" id="fromSaving" :to="{ name: 'saving' }">정기적금</RouterLink>
    </div>
    <div class="d-flex justify-content-between align-items-center my-2">
      <p>전체 {{ savingStore.saving.length }} 건</p>
      <form @submit.prevent="changeSaving" class="d-flex gap-2">
        <select v-model="category">
          <option value="all">은행전체</option>
          <option v-for="category in savingStore.categoryBank" :key="category" :value="category">
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
        <tr v-for="base in saving" :key="base.id">
          <td>{{ base.kor_co_nm }}</td>
          <td @click="detailSaving(base.fin_prdt_cd)" id="moveSavingDetail">{{ base.fin_prdt_nm }}</td>
          <td>
            {{
              base.savingoptions_set.find((item) => {
                return item.save_trm === 6;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.savingoptions_set.find((item) => {
                return item.save_trm === 12;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.savingoptions_set.find((item) => {
                return item.save_trm === 24;
              })?.intr_rate2 ?? "-"
            }}
          </td>
          <td>
            {{
              base.savingoptions_set.find((item) => {
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
import { RouterLink, useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import { useSavingStore } from "../stores/saving";

const savingStore = useSavingStore();
const router = useRouter();

const category = ref("all");
const period = ref("all");
const saving = ref(savingStore.saving);

onMounted(() => {
  if (!savingStore.saving.length) {
    savingStore.callDeposit();
  }
});

const changeSaving = () => {
  if (period.value === "all" && category.value === "all") {
    saving.value = savingStore.saving;
  } else {
    saving.value = savingStore.searchSaving(period.value, category.value);
  }
};

const detailSaving = (id) => {
  router.push({ name: "savingDetail", params: { savingId: id } });
};
</script>

<style scoped>
select {
  /* width: 100%; */
  border: 1px solid #5fb9a6;
  border-radius: 5px;
  padding: 5px 10px;
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

#fromSaving {
  color: #5fb9a6;
}

a {
  text-decoration-line: none;
  color: black;
}

#moveSavingDetail {
  cursor: pointer;
  font-weight: bold;
}
</style>
