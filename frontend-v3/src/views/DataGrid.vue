<template>
  <v-container>
    <v-card>
      <v-card-title>데이터 그리드</v-card-title>
      <v-card-subtitle>현재 대시보드에 포함된 차트의 원본 데이터입니다.</v-card-subtitle>
      <v-card-text>
        <div v-if="isLoading" class="text-center pa-8">
          <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
          <p class="mt-4 text-subtitle-1">데이터를 불러오는 중입니다...</p>
        </div>
        <v-expansion-panels v-else-if="chartData.length > 0" variant="accordion">
          <v-expansion-panel
            v-for="chart in chartData"
            :key="chart.chartId"
          >
            <v-expansion-panel-title>{{ chart.initialPrompt }}</v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-data-table
                :headers="chart.tableData.headers.map(h => ({ title: h, key: h }))"
                :items="chart.tableData.items"
                class="elevation-1"
                density="compact"
              ></v-data-table>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
        <div v-else class="text-center pa-8">
          <p>표시할 데이터가 없습니다. 대시보드에 차트를 추가해주세요.</p>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const isLoading = ref(false);
const chartData = ref([]);

const loadAllChartData = async () => {
  isLoading.value = true;
  try {
    // 1. Load dashboard layout
    const layoutResponse = await axios.get('/api/dashboards/1');
    const layout = layoutResponse.data.layout || [];

    if (layout.length === 0) {
      isLoading.value = false;
      return;
    }

    // 2. For each chart in layout, fetch its table data
    const dataPromises = layout.map(item => {
      return axios.post('/api/chart', { prompt: item.initialPrompt })
        .then(response => ({
          chartId: item.i,
          initialPrompt: item.initialPrompt,
          tableData: response.data.tableData,
        }))
        .catch(error => {
          console.error(`Failed to load data for chart: ${item.initialPrompt}`, error);
          return {
            chartId: item.i,
            initialPrompt: item.initialPrompt,
            tableData: { headers: [], items: [] }, // Return empty data on error
          };
        });
    });

    chartData.value = await Promise.all(dataPromises);

  } catch (error) {
    console.error("Failed to load dashboard layout:", error);
    alert("대시보드 레이아웃을 불러오는 데 실패했습니다.");
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadAllChartData();
});
</script>
