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
        .toSorted((a, b) => b.user.length - a.user.length)
        .splice(0, 5);
    });

    const categoryBank = computed(() => {
      return Array.from(
        new Set(
          deposit.value.map((item) => {
            return item.kor_co_nm;
          })
        )
      );
    });

    const searchDeposits = computed(() => {
      return (period, bank) => {
        if (period === "all") {
          return deposit.value.filter((item) => item.kor_co_nm === bank);
        } else if (bank === "all") {
          return deposit.value.filter((item) =>
            item.depositoptions_set.some((item) => item.save_trm == period)
          );
        } else {
          return deposit.value.filter(
            (item) =>
              item.kor_co_nm === bank &&
              item.depositoptions_set.some((item) => item.save_trm == period)
          );
        }
      };
    });

    return {
      callDeposit,
      deposit,
      popularDeposits,
      categoryBank,
      searchDeposits,
    };
  },
  { persist: true }
);
