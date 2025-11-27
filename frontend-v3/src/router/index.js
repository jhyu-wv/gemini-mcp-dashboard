import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    redirect: '/debug', // 시작 페이지를 /debug로 변경
  },
  {
    path: '/debug', // 디버그 페이지 라우트 추가
    name: 'Debug',
    component: () => import('../views/Debug.vue'), // ../views 사용
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'), // ../views 사용
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/Report.vue'), // ../views 사용
  },
  {
    path: '/data-grid', // 데이터 그리드 라우트 추가
    name: 'DataGrid',
    component: () => import('../views/DataGrid.vue'), // ../views 사용
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
