import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vant from 'vant';
import 'vant/lib/index.css';

const app = createApp(App).use(router).mount('#app')
app.use(Vant);
