import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FinancialView from "../views/FinancialView.vue";
import FinancialDetailView from "../views/FinancialDetailView.vue";
import CurrencyView from "../views/CurrencyView.vue";
import BankMapView from "../views/BankMapView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/financial",
      name: "financial",
      component: FinancialView,
    },
    {
      path: "/financial/:financialId",
      name: "financialDetail",
      component: FinancialDetailView,
    },
    {
      path: "/currency",
      name: "currency",
      component: CurrencyView,
    },
    {
      path: "/bankMap",
      name: "bankMap",
      component: BankMapView,
    },
  ],
});

export default router;
