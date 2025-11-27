<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>AI Dashboard v3</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tabs align-with-title>
        <v-tab to="/dashboard">대시보드</v-tab>
        <v-tab to="/report">보고서</v-tab>
        <v-tab to="/data-grid">데이터 그리드</v-tab> <!-- 새로운 탭 추가 -->
      </v-tabs>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
// Vue 3 Composition API: <script setup>을 사용하면 별도의 export 구문이 필요 없습니다.
</script>

<style>
.v-main {
  background-color: #f4f6f8;
}
</style>
