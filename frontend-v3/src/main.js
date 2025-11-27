import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import VueApexCharts from 'vue3-apexcharts';

const app = createApp(App);

app.use(router);
app.use(vuetify);
app.use(VueApexCharts);

app.mount('#app');
