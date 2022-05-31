<template>
  <form v-if="withButton" @submit="handleSubmit">
    <InputText type="text" v-model="search.value" class="searchbar mr-2" />
    <Button icon="pi pi-search" type="submit" />
  </form>
  <form v-else>
    <span class="p-input-icon-left">
      <i class="pi pi-search" />
      <InputText
        type="text"
        v-model="search.value"
        class="searchbar"
        placeholder="Search"
      />
    </span>
  </form>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import { useSearchStore } from '@/stores/search';

defineProps<{
  withButton: boolean;
}>();

const router = useRouter();
const search = useSearchStore();

const handleSubmit = (e: Event) => {
  e.preventDefault();
  if (!search.value) return;
  router.push({
    name: 'search',
    params: {
      query: search.value,
    },
  });
};
</script>
