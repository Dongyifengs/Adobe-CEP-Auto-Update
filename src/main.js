import Vue from 'vue';
import 'element-ui/lib/theme-chalk/index.css';
import ElementUI from 'element-ui';
import App from './App.vue';
import router from './router';


Vue.config.productionTip = false;
Vue.config.devtools = false;

Vue.use(ElementUI)

new Vue({
  router,
  el: '#app',
  render: h => h(App)
}).$mount('#app');
