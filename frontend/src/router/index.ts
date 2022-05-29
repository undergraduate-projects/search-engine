import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import SearchView from '@/views/SearchView.vue';
import CaseView from '@/views/CaseView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/search/:query',
      name: 'search',
      component: SearchView,
    },
    {
      path: '/case',
      name: 'case',
      component: CaseView,
    },
  ],
});

export default router;
