<template>
  <v-container>
    <v-card>
      <v-card-title>진단 및 점검 페이지</v-card-title>
      <v-card-text>
        <p>이 페이지는 애플리케이션의 각 기능이 정상적으로 동작하는지 확인하기 위한 것입니다.</p>

        <v-divider class="my-4"></v-divider>

        <div class="text-subtitle-1 mb-2">1. 백엔드 API 통신 테스트</div>
        <v-btn @click="testApiConnection" :loading="apiTest.loading">대시보드 API 호출</v-btn>
        <v-alert :type="apiTest.type" class="mt-3" v-if="apiTest.message !== '아직 테스트되지 않았습니다.'">
          {{ apiTest.message }}
        </v-alert>
        <v-alert type="info" class="mt-3" v-else>
          {{ apiTest.message }}
        </v-alert>

        <v-divider class="my-4"></v-divider>

        <div class="text-subtitle-1 mb-2">2. 대시보드 페이지 이동</div>
        <p>모든 기능이 정상이라면 아래 버튼을 눌러 대시보드로 이동하세요.</p>
        <v-btn to="/dashboard" color="primary">대시보드로 이동</v-btn>

      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const apiTest = ref({
  loading: false,
  message: '아직 테스트되지 않았습니다.',
  type: 'info', // info, success, error
});

const testApiConnection = async () => {
  apiTest.value.loading = true;
  apiTest.value.message = '백엔드에 /api/dashboards/1 요청을 보내는 중...';
  apiTest.value.type = 'info';
  try {
    const response = await axios.get('/api/dashboards/1');
    apiTest.value.message = 'API 호출 성공! 백엔드로부터 응답을 받았습니다.\n응답 데이터: ' + JSON.stringify(response.data);
    apiTest.value.type = 'success';
  } catch (error) {
    apiTest.value.message = 'API 호출 실패! 백엔드 서버가 실행 중인지, /api/dashboards/1 엔드포인트가 올바르게 작동하는지 확인하세요.\n에러: ' + error.message;
    apiTest.value.type = 'error';
  } finally {
    apiTest.value.loading = false;
  }
};
</script>
