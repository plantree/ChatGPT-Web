import { createApp } from 'vue'
import { createStore } from 'vuex'
import naive from "naive-ui";
import './style.css'
import App from './App.vue'

// create a new store instance
const store = createStore({
    state() {
        return {
            // global config
            server: import.meta.env.VITE_SERVER,
        }
    }
})
createApp(App)
    .use(store)
    .use(naive)
    .mount('#app')
