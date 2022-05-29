<template>
  <form class="searchbar" @submit="handleSubmit">
    <InputText type="text" v-model="searchValue" class="mr-2" />
    <Button icon="pi pi-search" type="submit" />
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const searchValue = ref('');

const handleSubmit = (e: Event) => {
  e.preventDefault();
  router.push({
    name: 'search',
    params: {
      query: searchValue.value,
    },
  });
};
</script>

<style scoped>
.searchbar {
  height: fit-content;
}
.p-inputtext {
  width: 65vh;
}
</style>
