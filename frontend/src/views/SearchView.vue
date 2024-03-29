<script setup lang="ts">
import { onMounted, provide, ref } from 'vue';
import { RouterLink } from 'vue-router';
import Card from 'primevue/card';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import Paginator from 'primevue/paginator';
import type { PageState } from 'primevue/paginator';
import ProgressSpinner from 'primevue/progressspinner';
import HeaderBar from '../components/HeaderBar.vue';
import { api } from '@/router/axios';
import { useSearchStore } from '@/stores/search';
import type { AxiosRequestConfig } from 'axios';
import { updateQueryKey } from '@/stores/injections';

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
          method: 'post',
          data: {
            query: search.query.keyword,
            offset: offset != undefined ? offset : search.result.offset,
            AJLB:
              search.query.AJLB && search.query.AJLB.length > 0
                ? search.query.AJLB
                : undefined,
            SPCX:
              search.query.SPCX && search.query.SPCX.length > 0
                ? search.query.SPCX
                : undefined,
            FGCY:
              search.query.FGCY && search.query.FGCY.length > 0
                ? search.query.FGCY
                : undefined,
            AH: search.query.AH ? search.query.AH : undefined,
            AY: search.query.AY ? search.query.AY : undefined,
            JBFY: search.query.JBFY ? search.query.JBFY : undefined,
            WSZL:
              search.query.WSZL && search.query.WSZL.length > 0
                ? search.query.WSZL
                : undefined,
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
provide(updateQueryKey, () => {
  request(0);
});
const onPage = (event: PageState) => {
  console.log(event);
  request(event.page);
  window.scrollTo(0, 0);
};
</script>

<template>
  <div class="main flex flex-column">
    <Toast />
    <HeaderBar />

    <ProgressSpinner v-if="loading" />
    <template v-else>
      <template v-if="search.result.data.length == 0">
        <div class="notfound">
          <img src="@/assets/question.png" class="mt-3" />
          <h3 class="mt-3">没有搜索到相关结果</h3>
        </div>
      </template>
      <div v-else class="results">
        <template v-for="item in search.result.data" :key="item.id">
          <RouterLink
            :to="{ name: 'case', params: { id: item.id } }"
            class="m-3 result-link"
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
                      v-for="field in [
                        '案件类别',
                        '审判程序',
                        '法官成员',
                        '案号',
                        '案由',
                        '经办法院',
                        '文书种类',
                      ]"
                      :key="field"
                    >
                      <div v-if="field in item.source['案例属性']">
                        <b>{{ field }}：</b
                        ><span v-html="item.source['案例属性'][field]"></span>
                      </div>
                      <div v-else-if="field in item.source['全文']['文首']">
                        <b>{{ field }}：</b
                        ><span
                          v-html="item.source['全文']['文首'][field]"
                        ></span>
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
    </template>
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
  width: 900px;
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
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    column-gap: 1rem;
    row-gap: 0.5rem;
    padding-top: 0.5rem;
  }
}

.results {
  margin-left: 4rem;
  display: flex;
  flex-direction: column;
  width: fit-content;

  .result-link {
    width: fit-content;
  }
}

.notfound {
  margin: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  img {
    width: 9rem;
    height: 9rem;
  }
  color: var(--text-color);
}
.p-paginator {
  background: none;
  margin-bottom: 1rem;
}
</style>
