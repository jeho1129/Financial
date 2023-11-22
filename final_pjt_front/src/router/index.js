import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import FinancialView from "../views/FinancialView.vue";
import DepositView from "../views/DepositView.vue";
import DepositDetailView from "../views/DepositDetailView.vue";
import SavingView from "../views/SavingView.vue";
import SavingDetailView from "../views/SavingDetailView.vue";
import FinancialDetailView from "../views/FinancialDetailView.vue";
import BankMapView from "../views/BankMapView.vue";
import PostListView from "../views/PostListView.vue";
import PostCreateView from "../views/PostCreateView.vue";
import PostDetailView from "../views/PostDetailView.vue";
import MyProfileView from "../views/MyProfileView.vue";

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
      path: "/deposit",
      name: "deposit",
      component: DepositView,
    },
    {
      path: "/deposit/:depositId",
      name: "depositDetail",
      component: DepositDetailView,
    },
    {
      path: "/saving",
      name: "saving",
      component: SavingView,
    },
    {
      path: "/saving/:savingId",
      name: "savingDetail",
      component: SavingDetailView,
    },
    {
      path: "/financial/:financialId",
      name: "financialDetail",
      component: FinancialDetailView,
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
      path: "/post/:postId",
      name: "postDetail",
      component: PostDetailView,
    },
    {
      path: "/myProfile",
      name: "myProfile",
      component: MyProfileView,
    },
  ],
});

export default router;
