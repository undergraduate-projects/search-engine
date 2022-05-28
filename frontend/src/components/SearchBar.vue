<template>
  <div>
    <InputText type="text" v-model="searchValue" class="mr-2" />
    <Button label="Search" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const searchValue = ref('');
</script>

<style scoped>
.p-inputtext {
  width: 65vh;
}
</style>
