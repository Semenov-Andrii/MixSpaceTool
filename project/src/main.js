import './assets/main.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import i18n from './i18n';

const app = createApp(App);
i18n.setup();

app.use(i18n.vueI18n);
app.use(router);

app.mount('#app');
