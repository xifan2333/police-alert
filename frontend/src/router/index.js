import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PoliceLocation from '../views/PoliceLocation.vue'
import Situation from '../views/Situation.vue'
import Cases from '../views/Cases.vue'
import Disputes from '../views/Disputes.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/police-location',
    name: 'PoliceLocation',
    component: PoliceLocation
  },
  {
    path: '/situation',
    name: 'Situation',
    component: Situation
  },
  {
    path: '/cases',
    name: 'Cases',
    component: Cases
  },
  {
    path: '/disputes',
    name: 'Disputes',
    component: Disputes
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
