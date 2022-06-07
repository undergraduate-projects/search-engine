<template>
  <div class="header m-2 flex">
    <RouterLink :to="{ name: 'home' }" class="logo flex align-items-center">
      <img class="image" src="@/assets/justice.png" />
      <div class="text">
        Case<br />
        Lookup
      </div>
    </RouterLink>
    <SearchBar :with-button="false" class="search" />
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import SearchBar from './SearchBar.vue';
</script>

<style scoped lang="scss">
.logo {
  .image {
    height: 5rem;
    margin-right: 0.2rem;
  }
  .text {
    font-size: 1.2rem;
    font-weight: 700;
    font-family: Verdana;
    color: #4e4f52;
  }
  margin-left: 1.1rem;
  margin-right: 3rem;
  height: fit-content;
}

.search {
  margin-top: 1.1rem;
  flex-grow: 1;
}

a:link {
  text-decoration: none;
}
</style>
