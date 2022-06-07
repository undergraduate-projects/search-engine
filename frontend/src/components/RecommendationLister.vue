<template>
  <div class="header">
    <div class="title">{{ title }}</div>
    <Button
      icon="pi pi-refresh"
      class="p-button-rounded p-button-text refresh"
      @click="refresh"
    />
  </div>

  <template
    v-for="(item, i) in data.slice(page * pageSize, (page + 1) * pageSize)"
    :key="i"
  >
    <div class="item">
      {{ page * pageSize + i + 1 }}
      <RouterLink :to="{ name: 'case', params: { id: item._id } }">
        {{ item._source['全文']['文首']['案号'] }}
      </RouterLink>
    </div>
  </template>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink } from 'vue-router';
import Button from 'primevue/button';

const props = defineProps<{
  title: string;
  data: any[];
}>();

const page = ref(0);
const pageSize = 5;

function refresh() {
  page.value = (page.value + 1) % Math.ceil(props.data.length / pageSize);
}
</script>

<style scoped lang="scss">
.header {
  display: flex;
  align-items: center;
  .title {
    font-size: 1rem;
    font-weight: 700;
  }
  .refresh {
    margin-left: auto;
    height: 2.2rem !important;
    width: 2.2rem !important;
  }
}
a:link {
  text-decoration: none;
  color: var(--text-color);
}
.item {
  margin: 0.5rem 0;
  a {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
</style>
