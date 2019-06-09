import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    { path: '/new',
      name: 'new',
      component: () => import(/* webpackChunkName: "new" */ './views/NewGame.vue')
    },
    { path: '/current-games',
      name: 'current-games',
      component: () => import(/* webpackChunkName: "current-games" */ './views/Games.vue')
    },
    { path: '*', name: '404', component: NotFound}
  ]
})
