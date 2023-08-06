import Vue from 'vue';
import App from './link_all.vue';


document.addEventListener('DOMContentLoaded', () => {
    new Vue({render: h => h(App)}).$mount('.form-row.field-link');
});
