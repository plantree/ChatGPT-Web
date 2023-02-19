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
            server: 'http://127.0.0.1:8000',
        }
    }
})
createApp(App)
    .use(store)
    .use(naive)
    .mount('#app')
