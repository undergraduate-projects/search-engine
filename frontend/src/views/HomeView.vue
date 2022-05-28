<script setup lang="ts">
import SearchBar from '@/components/SearchBar.vue';
</script>

<template>
  <div class="main flex flex-column">
    <div class="content flex flex-column align-items-center">
      <div class="logo flex align-items-center">
        <img class="image" src="@/assets/justice.png" />
        <div class="text">Case Lookup</div>
      </div>
      <SearchBar class="searchbar" />
    </div>
    <div>
      <svg
        class="waves"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 24 150 28"
        preserveAspectRatio="none"
        shape-rendering="auto"
      >
        <defs>
          <path
            id="gentle-wave"
            d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-352z"
          />
        </defs>
        <g class="parallax">
          <use
            xlink:href="#gentle-wave"
            x="48"
            y="0"
            fill="rgba(255,255,255,0.7"
          />
          <use
            xlink:href="#gentle-wave"
            x="48"
            y="3"
            fill="rgba(255,255,255,0.5)"
          />
          <use
            xlink:href="#gentle-wave"
            x="48"
            y="5"
            fill="rgba(255,255,255,0.3)"
          />
          <use xlink:href="#gentle-wave" x="48" y="7" fill="#fff" />
        </g>
      </svg>
    </div>
  </div>
  <div class="foot">
    搜索引擎技术基础 &nbsp;&nbsp; | &nbsp;&nbsp; 周天泽&nbsp; 王通泽
  </div>
</template>

<style scoped lang="scss">
.main {
  // background: linear-gradient(
  //   60deg,
  //   rgba(84, 58, 183, 1) 0%,
  //   rgba(0, 172, 193, 1) 100%
  // );
  // background-image: linear-gradient(0deg, #d9afd9 0%, #97d9e1 100%);
  background-image: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
}
.content {
  margin: 5rem auto;
  padding: 2rem;
  padding-bottom: 2.5rem;
  width: fit-content;
  background-color: rgba(255, 255, 255, 0.5);
  // backdrop-filter: blur(2px);
  border-radius: 1.5rem;
  // box-shadow: 5px 10px #888888;
  // box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.waves {
  position: relative;
  width: 100%;
  height: 10vh;
  margin-top: 3rem;
  margin-bottom: -7px; /*Fix for safari gap*/
  min-height: 90px;
  max-height: 150px;
}

.logo {
  margin-bottom: 2.5rem;
  .image {
    width: 10vw;
    margin-right: 1rem;
  }
  .text {
    font-size: 3rem;
    font-weight: bold;
    font-family: Verdana;
    color: #494a4c;
  }
}

.searchbar {
  height: fit-content;
}

.foot {
  width: fit-content;
  margin: auto;
  margin-top: 5rem;
  text-align: center;
  color: #aeb1b6;
}

/* Animation */
// https://codepen.io/goodkatz/pen/LYPGxQz

.parallax > use {
  animation: move-forever 25s cubic-bezier(0.55, 0.5, 0.45, 0.5) infinite;
}
.parallax > use:nth-child(1) {
  animation-delay: -2s;
  animation-duration: 7s;
}
.parallax > use:nth-child(2) {
  animation-delay: -3s;
  animation-duration: 10s;
}
.parallax > use:nth-child(3) {
  animation-delay: -4s;
  animation-duration: 13s;
}
.parallax > use:nth-child(4) {
  animation-delay: -5s;
  animation-duration: 20s;
}
@keyframes move-forever {
  0% {
    transform: translate3d(-90px, 0, 0);
  }
  100% {
    transform: translate3d(85px, 0, 0);
  }
}
/*Shrinking for mobile*/
@media (max-width: 768px) {
  .waves {
    height: 40px;
    min-height: 40px;
  }
  .content {
    height: 30vh;
  }
  h1 {
    font-size: 24px;
  }
}
</style>
