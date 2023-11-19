<template>
  <form @submit.prevent="changeSaving">
    <select v-model="period">
      <option value="all">전체상품</option>
      <option value="6">6개월</option>
      <option value="12">12개월</option>
      <option value="24">24개월</option>
      <option value="36">36개월</option>
    </select>
    <select v-model="category">
      <option value="all">전체</option>
      <option
        v-for="category in savingStore.categoryBank"
        :key="category"
        :value="category"
      >
        {{ category }}
      </option>
    </select>
    <button>적용</button>
  </form>
  <table class="table text-center">
    <thead>
      <tr class="table-success">
        <th scope="col">금융회사명aaaa</th>
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
        <td>{{ base.fin_prdt_nm }}</td>
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
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useSavingStore } from "../stores/saving";

const savingStore = useSavingStore();

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
</script>

<style scoped></style>
