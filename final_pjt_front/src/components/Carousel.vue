<template>
  <div>
    <div id="carouselExampleIndicators" class="carousel slide">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active position-relative">
          <img src="../../public/assets/c1.png" class="c1 d-block w-100" alt="..." />
        </div>
        <div class="carousel-item">
          <img src="../../public/assets/c2.webp" class="c2 d-block w-100" alt="..." />
        </div>
        <div class="carousel-item">
          <img src="../../public/assets/c3.jfif" class="c3 d-block w-100" alt="..." />
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
img.c1 {
  background-color: rgb(183, 127, 68);
  width: 350px;
  height: 350px;
  object-fit: contain;
}

img.c2 {
  background-color: #fba014;
  width: 350px;
  height: 350px;
  object-fit: contain;
}

img.c3 {
  background-color: #9a7deb;
  width: 350px;
  height: 350px;
  object-fit: contain;
}

.carousel-indicators button {
  height: 10px;
  width: 10px;
  border-radius: 50%;
}

p.c1 {
  position: absolute;
  z-index: 3;
  color: red;
}
</style>
