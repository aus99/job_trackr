import { createApp } from 'vue'
import router from "./router";
import App from "./App.vue";
import axios from "axios";
import './index.css'
import {AudioRecorder} from "vue-audio-recorder";

createApp(App).use(router, axios).mount('#app')
App.use(AudioRecorder)
