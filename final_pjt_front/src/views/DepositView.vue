<template>
  <div class="mt-5 container" id="depositMain">
    <div class="d-flex gap-2 align-items-center" id="depositHead">
      <RouterLink class="fs-4" id="fromDeposit" :to="{ name: 'deposit' }"
        >정기예금</RouterLink
      >
      |
      <RouterLink class="fs-4" :to="{ name: 'saving' }">정기적금</RouterLink>
    </div>
    <div class="d-flex justify-content-between align-items-center my-2">
      <p class="m-0">전체 {{ deposit.length }} 건</p>
      <form @submit.prevent="changeDeposit" class="d-flex gap-2">
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
    <table id="sort_table" class="table text-center">
      <thead>
        <tr class="table-success">
          <th scope="col">금융회사명</th>
          <th scope="col">상품명</th>
          <th scope="'col'">
            6개월
            <font-awesome-icon
              :icon="['fas', 'sort']"
              @click="sort(2)"
              style="cursor: pointer"
            />
          </th>
          <th scope="'col'">
            12개월
            <font-awesome-icon
              :icon="['fas', 'sort']"
              @click="sort(3)"
              style="cursor: pointer"
            />
          </th>
          <th scope="'col'">
            24개월
            <font-awesome-icon
              :icon="['fas', 'sort']"
              @click="sort(4)"
              style="cursor: pointer"
            />
          </th>
          <th scope="'col'">
            36개월
            <font-awesome-icon
              :icon="['fas', 'sort']"
              @click="sort(5)"
              style="cursor: pointer"
            />
          </th>
          <th v-if="authStore.user?.is_superuser" scope="col">변경</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="base in deposit" :key="base.id">
          <td>{{ base.kor_co_nm }}</td>
          <td @click="detailDeposit(base.fin_prdt_cd)" id="moveDepoitDetail">
            {{ base.fin_prdt_nm }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 6;
              })?.intr_rate ||
              base.depositoptions_set.find((item) => {
                return item.save_trm === 6;
              })?.intr_rate2 ||
              "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 12;
              })?.intr_rate ||
              base.depositoptions_set.find((item) => {
                return item.save_trm === 12;
              })?.intr_rate2 ||
              "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 24;
              })?.intr_rate ||
              base.depositoptions_set.find((item) => {
                return item.save_trm === 24;
              })?.intr_rate2 ||
              "-"
            }}
          </td>
          <td>
            {{
              base.depositoptions_set.find((item) => {
                return item.save_trm === 36;
              })?.intr_rate ||
              base.depositoptions_set.find((item) => {
                return item.save_trm === 36;
              })?.intr_rate2 ||
              "-"
            }}
          </td>
          <td v-if="authStore.user?.is_superuser">
            <button @click="changePassword(base)">변경</button>
          </td>
        </tr>
      </tbody>
    </table>
    <ChangeRate :deposit-data="depositData" id="moveChangeRate" />
  </div>
</template>

<script setup>
import { RouterLink, useRouter } from "vue-router";
import { onMounted, ref } from "vue";
import { useDepositStore } from "../stores/deposit";
import { useAuthStore } from "../stores/auth";
import ChangeRate from "../components/ChangeRate.vue";

const depositStore = useDepositStore();
const router = useRouter();
const authStore = useAuthStore();

const category = ref("all");
const period = ref("all");
const deposit = ref(depositStore.deposit);
const ck = ref([0, 0, 0, 0]);
const depositData = ref({});

const changePassword = (data) => {
  depositData.value = data;
  const dialog = document.querySelector("#moveChangeRate");
  dialog.showModal();
};

onMounted(() => {
  depositStore.callDeposit();
});

const changeDeposit = () => {
  if (period.value === "all" && category.value === "all") {
    deposit.value = depositStore.deposit;
  } else {
    deposit.value = depositStore.searchDeposits(period.value, category.value);
    // console.log(depositStore.searchDeposits(period.value, category.value));
  }
};

const detailDeposit = (id) => {
  router.push({ name: "depositDetail", params: { depositId: id } });
};

function sortDesc(table_id, sortColumn) {
  var tableData = document
    .getElementById(table_id)
    .getElementsByTagName("tbody")
    .item(0);
  var rowData = tableData.getElementsByTagName("tr");
  console.log(rowData.item(0));
  for (var i = 0; i < rowData.length - 1; i++) {
    for (var j = 0; j < rowData.length - (i + 1); j++) {
      if (
        Number(
          rowData
            .item(j)
            .getElementsByTagName("td")
            .item(sortColumn)
            .innerHTML.replace(/[^0-9\.]+/g, "")
        ) <
        Number(
          rowData
            .item(j + 1)
            .getElementsByTagName("td")
            .item(sortColumn)
            .innerHTML.replace(/[^0-9\.]+/g, "")
        )
      ) {
        tableData.insertBefore(rowData.item(j + 1), rowData.item(j));
      }
    }
  }
}

function sortAsc(table_id, sortColumn) {
  var tableData = document
    .getElementById(table_id)
    .getElementsByTagName("tbody")
    .item(0);
  var rowData = tableData.getElementsByTagName("tr");
  console.log(rowData.item(0));
  for (var i = 0; i < rowData.length - 1; i++) {
    for (var j = 0; j < rowData.length - (i + 1); j++) {
      if (
        Number(
          rowData
            .item(j)
            .getElementsByTagName("td")
            .item(sortColumn)
            .innerHTML.replace(/[^0-9\.]+/g, "")
        ) >
        Number(
          rowData
            .item(j + 1)
            .getElementsByTagName("td")
            .item(sortColumn)
            .innerHTML.replace(/[^0-9\.]+/g, "")
        )
      ) {
        tableData.insertBefore(rowData.item(j + 1), rowData.item(j));
      }
    }
  }
}
function sort(item) {
  // console.log(item);
  for (let index = 2; index < 6; index++) {
    if (index !== item) {
      // console.log(index);
      ck.value[index - 2] = 0;
    }
  }
  console.log(ck.value);
  if (ck.value[item - 2]) {
    sortDesc("sort_table", item);
    ck.value[item - 2] = 0;
  } else {
    sortAsc("sort_table", item);
    ck.value[item - 2] = 1;
  }
  // console.log(ck.value);
}
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
  font-weight: bolder;
}

button:hover {
  filter: brightness(0.9);
}

#fromDeposit {
  color: #5fb9a6;
  font-weight: bold;
}

a {
  text-decoration-line: none;
  color: black;
}

#moveDepoitDetail {
  cursor: pointer;
  font-weight: bold;
}
</style>
