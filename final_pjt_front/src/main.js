import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fas } from "@fortawesome/free-solid-svg-icons";

library.add(far, fas);

const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

// app.use(createPinia())
app.use(pinia);
app.use(router);

app.component("font-awesome-icon", FontAwesomeIcon).mount("#app");
