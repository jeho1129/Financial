<!-- ChartComponent.vue -->

<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";

// Chart.js 레지스터
Chart.register(...registerables);

const props = defineProps({});

// 차트 데이터
const chartData = ref({
  labels: ["Label 1", "Label 2", "Label 3"],
  datasets: [
    {
      label: "Dataset Label",
      data: [10, 20, 30],
    },
  ],
});

// 차트 생성
let chart;

onMounted(() => {
  const canvas = document.getElementById("chartCanvas");
  if (canvas) {
    chart = new Chart(canvas.getContext("2d"), {
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
