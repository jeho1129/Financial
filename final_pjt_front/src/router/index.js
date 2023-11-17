import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FinancialView from "../views/FinancialView.vue";
import FinancialDetailView from "../views/FinancialDetailView.vue";
import CurrencyView from "../views/CurrencyView.vue";
import BankMapView from "../views/BankMapView.vue";
import PostListView from "../views/PostListView.vue";
import PostCreateView from "../views/PostCreateView.vue";
import PostDetailView from "../views/PostDetailView.vue";

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
    {
      path: "/post",
      name: "post",
      component: PostListView,
    },
    {
      path: "/postCreate",
      name: "postCreate",
      component: PostCreateView,
    },
    {
      path: "/postDetail/:postId",
      name: "postDetail",
      component: PostDetailView,
    },
  ],
});

export default router;
