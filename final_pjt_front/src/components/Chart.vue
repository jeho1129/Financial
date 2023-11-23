<!-- ChartComponent.vue -->

<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";
import { useAuthStore } from "../stores/auth";

// Chart.js 레지스터
Chart.register(...registerables);

const authStore = useAuthStore();

const props = defineProps({
  findDeposit: Array,
  findSaving: Array,
});

// 차트 생성
const chart = ref("");

onMounted(() => {
  const canvas = document.getElementById("chartCanvas");

  // 차트 데이터
  const chartData = ref({
    labels: Object.values(authStore.user.financial_products).map(
      (item) => item.fin_prdt_nm
    ),
    datasets: [
      {
        label: "저축 금리",
        data: Object.values(authStore.user.financial_products).map((item) => {
          if (item?.depositoptions_set) {
            return (
              item.depositoptions_set?.intr_rate ??
              item.depositoptions_set.intr_rate2
            );
          } else {
            return (
              item.savingoptions_set?.intr_rate ??
              item.savingoptions_set.intr_rate2
            );
          }
        }),
        backgroundColor: ["rgba(255, 99, 132, 0.2)"],
        borderColor: ["rgba(255, 99, 132, 1)"],
        borderWidth: 1,
      },
      {
        label: "최고 우대금리",
        data: Object.values(authStore.user.financial_products).map((item) => {
          if (item?.depositoptions_set) {
            return item.depositoptions_set.intr_rate2;
          } else {
            return item.savingoptions_set.intr_rate2;
          }
        }),
        backgroundColor: ["rgba(75, 192, 192, 0.2)"],
        borderColor: ["rgba(75, 192, 192, 1)"],
        borderWidth: 1,
      },
    ],
  });

  if (canvas) {
    chart.value = new Chart(canvas.getContext("2d"), {
      type: "bar",
      data: chartData.value,
      options: {
        // 차트 옵션 설정
      },
    });
  }
});
</script>

<template>
  <div>
    <canvas id="chartCanvas"></canvas>
  </div>
</template>
