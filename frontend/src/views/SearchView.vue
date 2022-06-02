<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import Card from 'primevue/card';
import Tree from 'primevue/tree';
import type {
  TreeNode,
  TreeExpandedKeys,
  TreeSelectionKeys,
} from 'primevue/tree';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import HeaderBar from '../components/HeaderBar.vue';
import { api } from '@/router/axios';
import { useSearchStore } from '@/stores/search';

const toast = useToast();

const search = useSearchStore();
onMounted(() => {
  api
    .get('search', {
      params: {
        query: search.query,
        offset: 0,
      },
    })
    .then(({ data }) => {
      search.setResult(data);
    })
    .catch((error) => {
      console.error(error);
      toast.add({
        severity: 'error',
        summary: 'Request failed',
        detail: error.message,
        life: 3000,
      });
    });
});

const items = ref<TreeNode[]>([
  {
    key: '0',
    label: '审理法院',
    icon: 'pi pi-fw pi-building',
    children: [
      {
        key: '0-0',
        label: '最高人民法院',
      },
      {
        key: '0-1',
        label: '北京市高级人民法院',
        children: [
          { key: '0-1-0', label: '北京市第一中级人民法院' },
          { key: '0-1-1', label: '北京市第二中级人民法院' },
        ],
      },
    ],
  },
]);

function allKeys(items: TreeNode[]) {
  return items.reduce<TreeExpandedKeys>((keys, item) => {
    keys[item.key as string] = true;
    if (item.children) {
      Object.assign(keys, allKeys(item.children));
    }
    return keys;
  }, {});
}
const expandedKeys: TreeExpandedKeys = allKeys(items.value);

const selectedKeys = ref<TreeSelectionKeys>(
  Object.keys(expandedKeys).reduce<TreeSelectionKeys>((keys, key) => {
    keys[key] = { checked: true, partialChecked: false };
    return keys;
  }, {})
);
</script>

<template>
  <div class="main flex flex-column">
    <Toast />
    <HeaderBar />
    <div class="flex">
      <Tree
        class="sidebar ml-4 mr-3 mt-3 flex-shrink-0"
        :value="items"
        selectionMode="checkbox"
        :expandedKeys="expandedKeys"
        v-model:selectionKeys="selectedKeys"
      />

      <div class="results flex-grow-1">
        <RouterLink :to="{ name: 'case' }" class="m-3" v-for="n in 10" :key="n">
          <Card class="result">
            <template #title> Result Title </template>
            <template #content>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit.
              Inventore sed consequuntur error repudiandae numquam deserunt
              quisquam repellat libero asperiores earum nam nobis, culpa ratione
              quam perferendis esse, cupiditate neque quas!
            </template>
          </Card>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  background-color: #f7f7f7;
}

a:link {
  text-decoration: none;
}

:deep(.searchbar) {
  width: 65vh;
}

.sidebar {
  padding: 1rem;
  padding-left: 0.5rem;
  height: fit-content;
  max-width: 300px;
  border: none;
  border-radius: 10px;
  background: #f7f7f7;
  box-shadow: inset 5px 5px 8px #e8e8e8, inset -5px -5px 8px #ffffff;
  :deep(.p-checkbox) {
    height: 17px;
    width: 17px;
  }
  :deep(.p-checkbox-box) {
    height: 17px;
    width: 17px;
  }
  :deep(.p-checkbox-icon) {
    font-size: 9px !important;
  }
  :deep(.p-tree-toggler-icon) {
    font-size: 0.9rem !important;
  }
  :deep(.p-tree-toggler) {
    height: 1.7rem !important;
    width: 1.7rem !important;
  }
  :deep(.p-tree-container .p-treenode .p-treenode-content.p-highlight) {
    background: none !important;
    color: var(--text-color) !important;
  }
  :deep(.p-treenode-label) {
    font-size: 0.9rem;
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  :deep(.p-treenode-label):hover {
    overflow: visible;
    white-space: normal;
  }
}

.result {
  max-width: 900px;
  border-radius: 10px;
  background: #f7f7f7;
  box-shadow: 5px 5px 10px #ebebeb, -5px -5px 10px #ffffff;
}
</style>
