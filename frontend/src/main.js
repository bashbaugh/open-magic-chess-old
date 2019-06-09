import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import store from './store'

Vue.config.productionTip = false

new Vue({
  router,

  data: {
    connected: false
  },

  render: h => h(App),
  store,

  created: function() {
    document.title = "Open Magic Chess"
  }
}).$mount('#app')