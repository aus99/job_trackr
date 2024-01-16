import { createApp } from 'vue'
import DashboardView from './views/DashboardView.vue'
import router from "@/router";
import axios from "axios";

createApp(DashboardView).use(router, axios).mount('#app')
