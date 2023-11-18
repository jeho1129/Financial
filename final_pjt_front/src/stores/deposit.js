import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

export const useDepositStore = defineStore(
  "deposit",
  () => {
    const deposit = ref([]);

    const authStore = useAuthStore();

    const callDeposit = () => {
      axios({
        method: "get",
        url: `${authStore.API_URL}/banking/deposits/list/`,
      })
        .then((res) => {
          deposit.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const popularDeposits = computed(() => {
      return deposit.value
        .toSorted(
          (a, b) => b["depositreviews_count"] - a["depositreviews_count"]
        )
        .splice(0, 4);
    });

    return { callDeposit, deposit, popularDeposits };
  },
  { persist: true }
);
