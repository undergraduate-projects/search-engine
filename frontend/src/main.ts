import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-indigo/theme.css'; //theme
import 'primevue/resources/primevue.min.css'; //core css
import 'primeicons/primeicons.css'; //icons
import 'primeflex/primeflex.css'; //flexbox

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.use(PrimeVue);
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
app.component(Button.name, Button);
app.component(InputText.name, InputText);

app.mount('#app');
