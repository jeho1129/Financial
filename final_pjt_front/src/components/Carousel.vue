<template>
  <div>
    <div id="carouselExampleIndicators" class="carousel slide">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img
            src="https://png.pngtree.com/background/20230527/original/pngtree-bank-vault-doors-in-the-dark-room-and-two-doors-picture-image_2770672.jpg"
            class="d-block w-100"
            alt="..."
          />
        </div>
        <div class="carousel-item">
          <img
            src="https://png.pngtree.com/background/20230616/original/pngtree-3d-rendered-bank-vault-unlocked-revealing-rows-of-deposit-boxes-picture-image_3637507.jpg"
            class="d-block w-100"
            alt="..."
          />
        </div>
        <div class="carousel-item">
          <img
            src="https://png.pngtree.com/thumb_back/fw800/background/20230527/pngtree-metal-bank-vaults-and-doors-on-the-black-background-image_2658300.jpg"
            class="d-block w-100"
            alt="..."
          />
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
img {
  height: 350px;
  object-fit: cover;
}

.carousel-indicators button {
  height: 10px;
  width: 10px;
  border-radius: 50%;
}
</style>
