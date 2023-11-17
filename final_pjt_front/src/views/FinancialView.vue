<template>
  <div>
    <h1>금융상품 비교</h1>
    <table class="table text-center">
      <thead>
        <tr class="table-primary">
          <th scope="col">공시 제출월</th>
          <th scope="col">금융 회사명</th>
          <th scope="col">상품명</th>
          <!-- <th scope="'col'">6개월</th> -->
          <!-- <th scope="'col'">12개월</th>
          <th scope="'col'">24개월</th>
          <th scope="'col'">36개월</th> -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="base in store.baseList" :key="base.fin_prdt_cd">
          <td>{{ base.dcls_month }}</td>
          <td>{{ base.kor_co_nm }}</td>
          <td>{{ base.fin_prdt_nm }}</td>
          <td>{{ base.pr6 }}</td>
          <td></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useDepositStore } from "../stores/deposit";

const store = useDepositStore();

// onMounted(() => {
//   baseList.filter((baseItem) => {
//     baseItem.pr6 = optionList.find((optionItem) => {
//       return optionItem.fin_prdt_cd === baseItem.fin_prdt_cd && optionItem.save_trm == 6;
//     });
//     baseItem.pr12 = optionList.find((optionItem) => {
//       return optionItem.fin_prdt_cd === baseItem.fin_prdt_cd && optionItem.save_trm == 12;
//     });
//     baseItem.pr24 = optionList.find((optionItem) => {
//       return optionItem.fin_prdt_cd === baseItem.fin_prdt_cd && optionItem.save_trm == 24;
//     });
//     baseItem.pr36 = optionList.find((optionItem) => {
//       return optionItem.fin_prdt_cd === baseItem.fin_prdt_cd && optionItem.save_trm == 36;
//     });
//   });
//   // console.log(baseList);
// });
</script>

<style scoped></style>
