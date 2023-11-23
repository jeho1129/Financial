<template>
  <header id="headerheader">
    <nav class="navbar navbar-expand-md bg-white mt-0 py-4">
      <div class="container-fluid">
        <RouterLink to="/" class="navbar-brand" style="font-size: x-large; font-family: 'Vina Sans', sans-serif"
          ><img src="./assets/logo.png" id="logo"
        /></RouterLink>
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
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> 금융상품 비교 </a>
                <ul class="dropdown-menu">
                  <li data-bs-dismiss="offcanvas" aria-label="Close">
                    <RouterLink :to="{ name: 'deposit' }" class="dropdown-item">정기예금</RouterLink>
                  </li>
                  <li data-bs-dismiss="offcanvas" aria-label="Close">
                    <RouterLink :to="{ name: 'saving' }" class="dropdown-item">정기적금</RouterLink>
                  </li>
                </ul>
              </li>
              <!-- <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/deposit" class="nav-link">금융상품 비교</RouterLink>
              </li> -->
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
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false"> 마이페이지 </a>
                <ul class="dropdown-menu">
                  <li data-bs-dismiss="offcanvas" aria-label="Close">
                    <RouterLink :to="{ name: 'myProfile' }" class="dropdown-item">기본 정보 수정</RouterLink>
                  </li>
                  <!-- <li><a class="dropdown-item" href="#">기본 정보 수정</a></li> -->

                  <li data-bs-dismiss="offcanvas" aria-label="Close">
                    <RouterLink :to="{ name: 'recommendProduct' }" class="dropdown-item">상품 추천 받기</RouterLink>
                  </li>
                </ul>
              </li>
              <!-- <li class="nav-item" data-bs-dismiss="offcanvas" aria-label="Close">
                <RouterLink to="/myProfile" class="nav-link">마이페이지</RouterLink>
                <span class="nav-link" style="cursor: pointer">마이페이지</span>
              </li> -->
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
  <ExchangeRate id="moveExchangeRate" :exchange-data="exchangeData" />

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
import { ref } from "vue";
import axios from "axios";

const authStore = useAuthStore();

const exchangeData = ref([]);

const signUp = () => {
  const dialog = document.querySelector("#moveSignUpPage");
  dialog.showModal();
};

const logIn = () => {
  const dialog = document.querySelector("#moveLogInPage");
  dialog.showModal();
};

const exchangeRate = () => {
  axios({
    method: "get",
    url: `${authStore.API_URL}/banking/exchanges/`,
    headers: {
      Authorization: `Token ${authStore.token}`,
    },
  })
    .then((res) => {
      exchangeData.value = res.data;
      const dialog = document.querySelector("#moveExchangeRate");
      dialog.showModal();
    })
    .catch((err) => {
      console.log(err);
    });
};
</script>

<style scoped>
.nav-link:hover {
  color: #5fb9a6;
  font-weight: bold;
  /* text-decoration-line: underline;
  text-decoration-thickness: 5px;
  text-decoration-color: red; */
}

img {
  width: 100px;
}

ul.navbar-nav li.dropdown:hover > ul.dropdown-menu {
  display: block;
  margin: 0;
}

header {
  position: sticky;
  top: 0;
}

#headerheader {
  z-index: 9999;
}

#logo {
  width: 40px;
  border-radius: 50%;
}
</style>
