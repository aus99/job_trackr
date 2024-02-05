import { createRouter, createWebHistory} from 'vue-router'
import DashboardView from "@/views/DashboardView.vue";
import ReportsView from "@/views/ReportsView.vue";
import ReportDetailsView from "@/views/ReportDetailsView"


const routes = [
    {
        path: '/',
        name: 'dashboard',
        component: DashboardView
    },
    {
        path: '/reports',
        name: 'reports',
        component: ReportsView
    },
    {
        path: '/reports/:id',
        name: 'reportDetails',
        component: ReportDetailsView
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL)
    ,routes
});

export default router;