<template>
  <header>
    <nav class="navbar navbar-expand-md bg-body-tertiary mt-0 py-4">
      <div class="container-fluid">
        <RouterLink to="/" class="navbar-brand">Jiho Bank</RouterLink>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasNavbar"
          aria-controls="offcanvasNavbar"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header">
            <!-- <RouterLink to="/" class="navbar-brand" id="offcanvasNavbarLabel">Jiho Bank</RouterLink> -->
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Jiho Bank</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav me-auto mb-lg-0">
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/deposit" class="nav-link">금융상품 비교</RouterLink>
              </li>
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <!-- <RouterLink to="/currency" class="nav-link"
                  >환율계산기</RouterLink
                > -->
                <span @click="exchangeRate" class="nav-link" style="cursor: pointer">환율계산기</span>
              </li>
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/bankMap" class="nav-link">은행 지도</RouterLink>
              </li>
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/post" class="nav-link">게시판</RouterLink>
              </li>
            </ul>
            <ul v-if="!authStore.isAuthenticated" class="navbar-nav mb-lg-0">
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <span @click="signUp" class="nav-link" style="cursor: pointer">회원가입</span>
                <!-- <RouterLink to="/signUp" class="nav-link">회원가입</RouterLink> -->
              </li>
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <span @click="logIn" class="nav-link" style="cursor: pointer">로그인</span>
                <!-- <RouterLink to="/logIn" class="nav-link">로그인</RouterLink> -->
              </li>
            </ul>
            <ul v-else class="navbar-nav mb-lg-0">
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/myProfile" class="nav-link">마이페이지</RouterLink>
                <!-- <span class="nav-link" style="cursor: pointer">마이페이지</span> -->
              </li>
              <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <span @click="authStore.logOut" class="nav-link" style="cursor: pointer">로그아웃</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </header>
  <SignUp id="moveSignUpPage" />
  <LogIn id="moveLogInPage" />
  <ExchangeRate id="moveExchangeRate" />

  <RouterView />
  <!-- style="height: 90vh" -->
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import SignUp from "./components/SignUp.vue";
import LogIn from "./components/LogIn.vue";
import Nav from "./components/Nav.vue";
import { useAuthStore } from "./stores/auth";
import ExchangeRate from "./components/ExchangeRate.vue";

const authStore = useAuthStore();

const signUp = () => {
  const dialog = document.querySelector("#moveSignUpPage");
  dialog.showModal();
};

const logIn = () => {
  const dialog = document.querySelector("#moveLogInPage");
  dialog.showModal();
};

const exchangeRate = () => {
  const dialog = document.querySelector("#moveExchangeRate");
  dialog.showModal();
};
</script>

<style scoped>
.nav-link:hover {
  color: #5fb9a6;
  /* text-decoration-line: underline;
  text-decoration-thickness: 5px;
  text-decoration-color: red; */
}

img {
  width: 100px;
}
</style>
