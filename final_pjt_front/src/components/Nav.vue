<template>
  <nav class="navbar bg-body-tertiary navbar-expand-lg">
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
      <div
        class="offcanvas offcanvas-end"
        tabindex="-1"
        id="offcanvasNavbar"
        aria-labelledby="offcanvasNavbarLabel"
      >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Jiho Bank</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="offcanvas"
            aria-label="Close"
          ></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav me-auto mb-lg-0">
            <li class="nav-item">
              <RouterLink to="/financial" class="nav-link"
                >금융상품 비교</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/currency" class="nav-link"
                >환율계산기</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink to="/bankMap" class="nav-link">은행 지도</RouterLink>
            </li>
          </ul>
          <ul class="navbar-nav mb-lg-0">
            <li class="nav-item">
              <span @click="signUp" class="nav-link" style="cursor: pointer"
                >회원가입</span
              >
              <!-- <RouterLink to="/signUp" class="nav-link">회원가입</RouterLink> -->
            </li>
            <li class="nav-item">
              <span @click="logIn" class="nav-link" style="cursor: pointer"
                >로그인</span
              >
              <!-- <RouterLink to="/logIn" class="nav-link">로그인</RouterLink> -->
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup></script>

<style scoped></style>
