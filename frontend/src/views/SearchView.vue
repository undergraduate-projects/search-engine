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
import Paginator from 'primevue/paginator';
import type { PageState } from 'primevue/paginator';
import ProgressSpinner from 'primevue/progressspinner';
import HeaderBar from '../components/HeaderBar.vue';
import { api } from '@/router/axios';
import { useSearchStore } from '@/stores/search';
import type { AxiosRequestConfig } from 'axios';

const toast = useToast();

const loading = ref(false);
const search = useSearchStore();
const request = (offset?: number) => {
  loading.value = true;
  const apiParams: AxiosRequestConfig = (() => {
    switch (search.query.type) {
      case 'keyword':
        return {
          url: 'search',
          method: 'get',
          params: {
            query: search.query.keyword,
            offset: offset != undefined ? offset : search.result.offset,
          },
        };
      case 'file':
        return {
          url: 'search-by-case',
          method: 'post',
          data: {
            xml_str: search.query.content,
            offset: offset != undefined ? offset : search.result.offset,
          },
        };
    }
  })();
  api(apiParams)
    .then(({ data }) => {
      search.result = data;
    })
    .catch((error) => {
      console.error(error);
      toast.add({
        severity: 'error',
        summary: 'Request failed',
        detail: error.message,
        life: 3000,
      });
    })
    .then(() => {
      loading.value = false;
    });
};
onMounted(() => request());
// onBeforeRouteUpdate(() => request(0));
const onSubmit = () => request(0);
const onPage = (event: PageState) => {
  console.log(event);
  request(event.page);
  window.scrollTo(0, 0);
};

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
    <HeaderBar @submit="onSubmit" />
    <div class="flex">
      <Tree
        class="sidebar ml-4 mr-3 mt-3 flex-shrink-0"
        :value="items"
        selectionMode="checkbox"
        :expandedKeys="expandedKeys"
        v-model:selectionKeys="selectedKeys"
      />
      <ProgressSpinner v-if="loading" />
      <div v-else class="flex flex-column">
        <template v-for="item in search.result.data" :key="item.id">
          <RouterLink
            :to="{ name: 'case', params: { id: item.id } }"
            class="m-3"
          >
            <Card class="result">
              <template #title>
                <span
                  v-html="
                    ('经办法院' in item.source['全文']['文首']
                      ? item.source['全文']['文首']['经办法院']
                      : item.source['全文']['文首']['承办机关']) +
                    ' ' +
                    ('文书名称' in item.source['全文']['文首']
                      ? item.source['全文']['文首']['文书名称']
                      : item.source['全文']['文首']['文书种类']) +
                    ' ' +
                    item.source['全文']['文首']['案号']
                  "
                />
              </template>
              <template #content>
                <div class="result-content">
                  <template v-for="(value, key) in item.highlight" :key="key">
                    <template v-for="(v, i) in value" :key="`${key}${i}`">
                      <div v-html="v" class="field" />
                    </template>
                  </template>
                  <div v-if="item.highlight == undefined">
                    {{ item.source['全文']['诉讼记录'] }}
                  </div>
                  <div class="property">
                    <template
                      v-for="field in ['案件类别', '案由']"
                      :key="field"
                    >
                      <div v-if="field in item.source['案例属性']">
                        <b>{{ field }}：</b
                        ><span v-html="item.source['案例属性'][field]"></span>
                      </div>
                    </template>
                  </div>
                </div>
              </template>
            </Card>
          </RouterLink>
        </template>
        <Paginator
          :rows="10"
          :totalRecords="search.result.total"
          @page="onPage"
          :first="search.result.offset * 10"
        ></Paginator>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  background-color: #f7f7f7;
  min-height: 100vh;
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

.p-progress-spinner {
  margin: 7rem auto;
  width: 5rem;
  :deep(.p-progress-spinner-circle) {
    stroke: var(--primary-color);
    // disable color animation: p-progress-spinner-color 6s ease-in-out infinite
    animation: p-progress-spinner-dash 1.5s ease-in-out infinite;
  }
}

.result {
  max-width: 900px;
  border-radius: 10px;
  background: #f7f7f7;
  box-shadow: 5px 5px 10px #ebebeb, -5px -5px 10px #ffffff;

  :deep(.p-card-content) {
    padding: 0.5rem 0 0 0;
  }

  :deep(.p-card-title) {
    font-size: 1.35rem;
  }
}

:deep(.result-content) {
  line-height: 1.5;
  .field {
    margin: 5px 0;
  }
  em {
    font-style: normal;
    background-color: rgb(255, 222, 180);
    padding: 1px 3px;
    margin: 2px;
    border-radius: 5px;
  }
  .property {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    padding-top: 0.5rem;
  }
}

.p-paginator {
  background: none;
  margin-bottom: 1rem;
}
</style>
