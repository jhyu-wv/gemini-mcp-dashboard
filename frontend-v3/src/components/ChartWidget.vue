<template>
  <v-card flat height="100%" class="d-flex flex-column">
    <v-card-title class="pa-2">
      <span class="text-subtitle-1">{{ chartTitle }}</span>
      <v-spacer></v-spacer>
      <v-btn icon="mdi-close" size="small" @click="emit('remove')"></v-btn>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="flex-grow-1 d-flex align-center justify-center">
      <div v-if="isLoading" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-2">AI가 차트를 생성 중입니다...</p>
      </div>
      <div v-else-if="error" class="text-center text-red">
        <v-icon icon="mdi-alert-circle-outline" color="red" class="mb-2"></v-icon>
        <p>{{ error }}</p>
      </div>
      <apexchart
        v-if="series.length > 0 && chartOptions.chart && chartOptions.chart.type"
        ref="chartRef"
        :type="chartOptions.chart.type"
        width="100%"
        height="100%"
        :options="chartOptions"
        :series="series"
      ></apexchart>
      <div v-else-if="!isLoading && !error" class="text-center text-grey">
        <p>차트 데이터가 없습니다.</p>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  chartId: {
    type: String,
    default: null,
  },
  initialPrompt: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['remove']);

const chartOptions = ref({
  chart: {
    type: '', // 초기값을 빈 문자열로 설정
  },
  xaxis: {
    categories: [],
  },
});
const series = ref([]);
const isLoading = ref(false);
const error = ref(null);
const chartTitle = ref('새 차트');
const chartRef = ref(null); // Ref for the apexchart component

const generateChart = async () => {
  if (!props.initialPrompt) {
    error.value = "차트를 생성할 프롬프트가 없습니다.";
    return;
  }
  isLoading.value = true;
  error.value = null;
  chartTitle.value = props.initialPrompt.length > 25 ? props.initialPrompt.substring(0, 22) + '...' : props.initialPrompt;

  try {
    const response = await axios.post('/api/chart', { prompt: props.initialPrompt });
    chartOptions.value = response.data.chartOptions;
    series.value = response.data.series;
  } catch (err) {
    console.error("차트 데이터 생성 실패:", err);
    error.value = "차트 생성에 실패했습니다. 백엔드 서버와 GOOGLE_API_KEY 설정을 확인해주세요.";
    series.value = []; // 에러 발생 시 기존 차트 제거

    // API 호출 실패 시 임시 데이터로 차트 표시 (디버깅용)
    console.warn("API 호출 실패, 임시 데이터로 차트 표시 시도.");
    chartOptions.value = {
      chart: { type: 'bar' },
      xaxis: { categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May'] }
    };
    series.value = [{
      name: '샘플 데이터 (API 실패)',
      data: [10, 20, 15, 25, 22]
    }];
    error.value += " (임시 데이터 표시)";

  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  if (props.initialPrompt) {
    generateChart();
  } else {
    error.value = "표시할 차트 정보가 없습니다.";
  }
});

const exportChartImage = async () => {
  if (chartRef.value && chartRef.value.chart) {
    return await chartRef.value.chart.dataURI().then(({ imgURI }) => {
      return imgURI;
    });
  }
  return null;
};

// Expose chartRef so parent can access it for resizing
defineExpose({
  chart: chartRef, // Expose the chart instance
  exportChartImage, // Expose the image export function
});
</script>

<style scoped>
.v-card-text {
  position: relative;
  height: calc(100% - 48px); /* v-card-title 높이 제외 */
}
.apexcharts-canvas {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
