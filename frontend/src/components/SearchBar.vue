<template>
  <form class="searchbar" @submit="handleSubmit">
    <InputText type="text" v-model="searchValue" class="mr-2" />
    <Button icon="pi pi-search" type="submit" />
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

const router = useRouter();
const searchValue = ref('');

const handleSubmit = (e: Event) => {
  e.preventDefault();
  if (!searchValue.value) return;
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
