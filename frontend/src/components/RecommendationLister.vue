<template>
  <div class="header">
    <div class="title">{{ title }}</div>
    <Button
      icon="pi pi-chevron-left"
      class="p-button-rounded p-button-text refresh prev"
      @click="prev"
    />
    <Button
      icon="pi pi-chevron-right"
      class="p-button-rounded p-button-text refresh"
      @click="next"
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

const pageNum = Math.ceil(props.data.length / pageSize);

function next() {
  if (page.value + 1 >= pageNum) return;
  page.value++;
}
function prev() {
  if (page.value <= 0) return;
  page.value--;
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
    height: 2.2rem !important;
    width: 2.2rem !important;
  }
  .prev {
    margin-left: auto;
  }
}
a:link {
  text-decoration: none;
  color: var(--text-color);
}
.item {
  margin: 0.5rem 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
