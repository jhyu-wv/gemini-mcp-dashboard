<template>
  <v-container fluid>
    <!-- 컨트롤 패널 -->
    <v-card class="mb-4">
      <v-card-text class="d-flex align-center">
        <v-textarea
          v-model="newChartPrompt"
          label="차트 생성 프롬프트 (예: 월간 이용 내역을 라인 차트로)"
          rows="1"
          auto-grow
          hide-details
          variant="outlined"
          class="mr-4"
        ></v-textarea>
        <v-btn color="primary" @click="addChartWidget" :loading="isAdding">
          차트 추가
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="blue-grey" class="white--text" @click="saveLayout" :loading="isSaving">
          <v-icon icon="mdi-content-save" left></v-icon>
          레이아웃 저장
        </v-btn>
        <v-btn color="teal" class="white--text ml-2" @click="downloadDashboardImage">
          <v-icon icon="mdi-camera" left></v-icon>
          이미지로 다운로드
        </v-btn>
        <v-btn color="purple" class="white--text ml-2" @click="generateReport">
          <v-icon icon="mdi-file-document-outline" left></v-icon>
          보고서 생성
        </v-btn>
      </v-card-text>
    </v-card>

    <!-- 대시보드 그리드 -->
    <grid-layout
      id="dashboard-grid"
      v-model:layout="layout"
      :col-num="12"
      :row-height="30"
      :is-draggable="true"
      :is-resizable="true"
      :vertical-compact="true"
      :use-css-transforms="true"
    >
      <grid-item
        v-for="item in layout"
        :key="item.i"
        :x="item.x"
        :y="item.y"
        :w="item.w"
        :h="item.h"
        :i="item.i"
        @resized="resizedEvent"
        class="widget-container"
      >
        <ChartWidget
          :ref="el => { if (el) chartRefs[item.i] = el }"
          :chart-id="item.i"
          :initial-prompt="item.initialPrompt"
          @remove="removeWidget(item.i)"
        />
      </grid-item>
    </grid-layout>
  </v-container>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { GridLayout, GridItem } from 'vue3-grid-layout';
import html2canvas from 'html2canvas';
import axios from 'axios';
import ChartWidget from '../components/ChartWidget.vue';
import { useRouter } from 'vue-router'; // Import useRouter

const layout = ref([]);
const newChartPrompt = ref('');
const isAdding = ref(false);
const isSaving = ref(false);
const router = useRouter(); // Initialize router

// For dynamic refs in Vue 3 Composition API
const chartRefs = reactive({});

const loadLayout = async () => {
  try {
    const response = await axios.get('/api/dashboards/1');
    layout.value = response.data.layout || [];
  } catch (error) {
    console.error("레이아웃 로딩 실패:", error);
    alert("레이아웃 로딩에 실패했습니다. 백엔드 서버가 실행 중인지 확인해주세요.");
  }
};

const saveLayout = async () => {
  isSaving.value = true;
  try {
    await axios.post('/api/dashboards/1', { layout: layout.value });
    alert("레이아웃이 저장되었습니다.");
  } catch (error) {
    console.error("레이아웃 저장 실패:", error);
    alert("레이아웃 저장에 실패했습니다.");
  } finally {
    isSaving.value = false;
  }
};

const downloadDashboardImage = () => {
  const dashboardElement = document.getElementById('dashboard-grid');
  alert("대시보드 이미지를 생성합니다. 잠시만 기다려주세요...");
  html2canvas(dashboardElement, { useCORS: true }).then(canvas => {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'dashboard.png';
    link.click();
  });
};

const addChartWidget = () => {
  if (!newChartPrompt.value) {
    alert("차트 생성 프롬프트를 입력해주세요.");
    return;
  }
  isAdding.value = true;
  const newItem = {
    x: (layout.value.length * 6) % 12,
    y: Infinity, // 아이템을 맨 아래에 추가
    w: 6,
    h: 8,
    i: Date.now().toString(),
    chartId: null, // 처음에는 chartId가 없음
    initialPrompt: newChartPrompt.value, // 프롬프트를 전달
  };
  layout.value.push(newItem);
  newChartPrompt.value = '';
  isAdding.value = false;
};

const removeWidget = (id) => {
  const index = layout.value.findIndex(item => item.i === id);
  if (index > -1) {
    layout.value.splice(index, 1);
  }
};

const resizedEvent = (i, newH, newW, newHPx, newWPx) => {
  // ApexCharts는 컨테이너 크기가 변경될 때 자동으로 리사이즈되지 않는 경우가 있음
  // 강제로 차트 리사이즈를 트리거
  const chartRef = chartRefs[i];
  if (chartRef && chartRef.chart) { // Assuming ChartWidget exposes 'chart' directly or via a method
    chartRef.chart.updateOptions({});
  }
};

const generateReport = async () => {
  const capturedCharts = [];
  for (const item of layout.value) {
    const chartWidgetRef = chartRefs[item.i];
    if (chartWidgetRef && chartWidgetRef.exportChartImage) {
      const imageData = await chartWidgetRef.exportChartImage();
      capturedCharts.push({
        chartId: item.i,
        initialPrompt: item.initialPrompt,
        imageData: imageData,
      });
    }
  }
  localStorage.setItem('capturedChartsForReport', JSON.stringify(capturedCharts));
  router.push('/report');
};

onMounted(() => {
  loadLayout();
});
</script>

<style>
.vue-grid-layout {
  background: #eee;
}
.vue-grid-item:not(.vue-grid-placeholder) {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}
.widget-container {
  overflow: hidden; /* 차트가 위젯 밖으로 나가지 않도록 */
}
</style>
