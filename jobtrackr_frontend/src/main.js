import { createApp } from 'vue'
import router from "./router";
import App from "./App.vue";
import axios from "axios";
import './index.css'

createApp(App).use(router, axios).mount('#app')
