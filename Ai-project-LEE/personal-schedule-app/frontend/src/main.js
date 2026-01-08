import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VCalendar from 'v-calendar';
import 'v-calendar/dist/style.css'; // Import V-Calendar CSS

const app = createApp(App)

app.use(router)
app.use(VCalendar, {}) // Use V-Calendar
app.mount('#app')