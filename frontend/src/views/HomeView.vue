<script setup lang="ts">
import SearchBar from '@/components/SearchBar.vue';
</script>

<template>
  <div class="bg h-screen w-screen absolute top-0 left-0" />
  <div class="content flex flex-column align-items-center">
    <div class="logo flex align-items-center">
      <img class="image" src="@/assets/justice.png" />
      <div class="text">Case Search</div>
    </div>
    <SearchBar class="searchbar" />
  </div>
</template>

<style scoped lang="scss">
.bg {
  background-image: url('https://images.pexels.com/photos/2935910/pexels-photo-2935910.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
  background-repeat: no-repeat;
  background-size: cover;
  // filter: blur(4px);
  z-index: -1;
}

.content {
  margin: 5rem auto;
  padding: 2rem;
  padding-bottom: 2.5rem;
  width: fit-content;
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(6px);
  border-radius: 1.5rem;
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
</style>
