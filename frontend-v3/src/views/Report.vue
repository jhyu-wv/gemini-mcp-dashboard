<template>
  <v-container>
    <v-card class="mb-6">
      <v-card-title class="d-flex align-center">
        AI 보고서
        <v-spacer></v-spacer>
        <v-btn color="teal" class="text-white" @click="downloadReport" :disabled="reportItems.length === 0">
          <v-icon prepend-icon="mdi-download"></v-icon>
          보고서 다운로드
        </v-btn>
      </v-card-title>
    </v-card>

    <div v-if="isLoading" class="text-center pa-8">
      <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
      <p class="mt-4 text-subtitle-1">AI가 보고서를 작성 중입니다. 잠시만 기다려주세요...</p>
    </div>

    <div v-else-if="reportItems.length > 0" class="report-page mx-auto">
      <div v-for="(item, index) in reportItems" :key="item.chartId" class="mb-8">
        <h2 class="text-h5 font-weight-bold mb-4">{{ item.initialPrompt }}</h2>
        <v-img :src="item.imageData" class="mb-4 elevation-2" max-height="400px" contain></v-img>
        <div v-html="marked(item.analysis)" class="markdown-body"></div>
      </div>
    </div>

    <v-card v-else class="report-page mx-auto">
      <v-card-text class="text-center text-h6">
        생성된 보고서 내용이 없습니다. 대시보드에서 차트를 추가하고 "보고서 생성" 버튼을 눌러주세요.
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { marked } from 'marked';
import { ref, onMounted } from 'vue';

const reportItems = ref([]);
const isLoading = ref(false);

const fetchReportAnalysis = async () => {
  isLoading.value = true;
  reportItems.value = []; // Clear previous items

  const capturedChartsJson = localStorage.getItem('capturedChartsForReport');
  if (!capturedChartsJson) {
    isLoading.value = false;
    return;
  }

  const capturedCharts = JSON.parse(capturedChartsJson);

  // Call backend API for each chart to get its analysis
  const analysisPromises = capturedCharts.map(async (chart) => {
    try {
      const response = await axios.post('/api/report', {
        prompt: chart.initialPrompt,
      });
      return {
        chartId: chart.chartId,
        initialPrompt: chart.initialPrompt,
        imageData: chart.imageData,
        analysis: response.data.analysis || "분석 내용을 가져오지 못했습니다.",
      };
    } catch (error) {
      console.error(`Error fetching analysis for chart ${chart.chartId}:`, error);
      return {
        chartId: chart.chartId,
        initialPrompt: chart.initialPrompt,
        imageData: chart.imageData,
        analysis: `### ${chart.initialPrompt} 분석 중 오류 발생\n\n- ${error.message || '알 수 없는 오류'}`,
      };
    }
  });

  reportItems.value = await Promise.all(analysisPromises);
  isLoading.value = false;
  localStorage.removeItem('capturedChartsForReport'); // Clear after use
};

const downloadReport = () => {
  let fullReportText = `# AI 대시보드 분석 보고서\n\n`;
  reportItems.value.forEach(item => {
    fullReportText += `## ${item.initialPrompt}\n\n`;
    fullReportText += `[차트 이미지: ${item.initialPrompt}]\n\n`; // Placeholder for image in text report
    fullReportText += `${item.analysis}\n\n`;
    fullReportText += `---\n\n`;
  });

  const blob = new Blob([fullReportText], { type: 'text/plain;charset=utf-8' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `AI_Dashboard_Report_${new Date().toISOString().slice(0, 10)}.txt`;
  link.click();
  URL.revokeObjectURL(link.href);
};

onMounted(() => {
  fetchReportAnalysis();
});
</script>

<style>
.report-page {
  background: white;
  width: 210mm;
  min-height: 297mm;
  padding: 20mm;
  margin: 1rem auto;
  box-shadow: 0 0 0.5cm rgba(0,0,0,0.5);
}

/* GitHub-like markdown style for better readability */
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #24292e;
}
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
  padding-bottom: .3em;
  border-bottom: 1px solid #eaecef;
}
.markdown-body h1 { font-size: 2em; }
.markdown-body h2 { font-size: 1.5em; }
.markdown-body h3 { font-size: 1.25em; }
.markdown-body ul {
  padding-left: 2em;
}
.markdown-body code {
  padding: .2em .4em;
  margin: 0;
  font-size: 85%;
  background-color: rgba(27,31,35,.05);
  border-radius: 3px;
}

@media print {
  body, .report-page {
    margin: 0;
    box-shadow: none;
  }
}
</style>
