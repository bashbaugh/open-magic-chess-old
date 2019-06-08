import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
  created: function() {
    document.title = "Open Magic Chess"
  }
}).$mount('#app')
