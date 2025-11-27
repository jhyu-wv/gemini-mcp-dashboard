<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        POPULATOR 데이터 그리드
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="검색"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        :items="data"
        :search="search"
        :loading="loading"
        loading-text="데이터 로딩 중..."
        no-data-text="데이터가 없습니다."
        class="elevation-1"
      >
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="deleteItem(item)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const search = ref('');
const data = ref([]);
const loading = ref(true);
const headers = ref([]);

const loadData = async () => {
  loading.value = true;
  try {
    const response = await axios.get('/api/data/populator');
    data.value = response.data;
    if (response.data.length > 0) {
      // 동적으로 헤더 생성
      headers.value = Object.keys(response.data[0]).map(key => ({
        title: key,
        align: 'start',
        sortable: true,
        key: key,
      }));
      // 액션 컬럼 추가 (필요하다면)
      // headers.value.push({ title: 'Actions', key: 'actions', sortable: false });
    }
  } catch (error) {
    console.error("POPULATOR 데이터 로딩 실패:", error);
    alert("데이터를 불러오는 데 실패했습니다.");
  } finally {
    loading.value = false;
  }
};

const editItem = (item) => {
  alert(`Edit item: ${JSON.stringify(item)}`);
  // 실제 편집 로직 구현
};

const deleteItem = (item) => {
  alert(`Delete item: ${JSON.stringify(item)}`);
  // 실제 삭제 로직 구현
};

onMounted(() => {
  loadData();
});
</script>

<style scoped>
/* 필요한 스타일 추가 */
</style>
