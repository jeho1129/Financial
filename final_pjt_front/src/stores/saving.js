import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

export const useSavingStore = defineStore(
  "saving",
  () => {
    const saving = ref([]);

    const authStore = useAuthStore();

    const callSaving = () => {
      axios({
        method: "get",
        url: `${authStore.API_URL}/banking/savings/list/`,
      })
        .then((res) => {
          console.log(res.data);
          saving.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    };

    const popularSaving = computed(() => {
      return saving.value
        .toSorted((a, b) => b.user.length - a.user.length)
        .splice(0, 5);
    });

    const categoryBank = computed(() => {
      return Array.from(
        new Set(
          saving.value.map((item) => {
            return item.kor_co_nm;
          })
        )
      );
    });

    const searchSaving = computed(() => {
      return (period, bank) => {
        if (period === "all") {
          return saving.value.filter((item) => item.kor_co_nm === bank);
        } else if (bank === "all") {
          return saving.value.filter((item) =>
            item.savingoptions_set.some((item) => item.save_trm == period)
          );
        } else {
          return saving.value.filter(
            (item) =>
              item.kor_co_nm === bank &&
              item.savingoptions_set.some((item) => item.save_trm == period)
          );
        }
      };
    });

    return {
      saving,
      callSaving,
      popularSaving,
      categoryBank,
      searchSaving,
    };
  },
  { persist: true }
);
