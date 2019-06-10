import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
import store from './store'
import VueSocketIO from 'vue-socket.io';

Vue.config.productionTip = false

Vue.use(new VueSocketIO({
  debug: true,
  connection: '`//${window.location.hostname}:80`',
  vuex: {
    store,
    actionPrefix: 'SOCKET_',
  },
}))

new Vue({
  router,
  render: h => h(App),
  store,
  created: function() {
    document.title = "Open Magic Chess"
  }
}).$mount('#app')
