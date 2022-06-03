<script setup lang="ts">
import HeaderBar from '../components/HeaderBar.vue';
import Toast from 'primevue/toast';
import { useSearchStore } from '@/stores/search';
import { useRoute } from 'vue-router';

const search = useSearchStore();
const route = useRoute();
const item = search.result.data.find((item) => item.id === route.params.id);

const casea = item ? item.source : {};
</script>

<template>
  <div class="main flex flex-column">
    <Toast />
    <HeaderBar />
    <div class="body">
      <div class="content">
        <h1 style="text-align: center">
          {{
            ('经办法院' in casea.全文.文首
              ? casea.全文.文首.经办法院
              : casea.全文.文首.承办机关) +
            ' ' +
            casea.全文.文首.文书名称
          }}
        </h1>
        <h2 style="text-align: center">{{ casea.全文.文首.案号 }}</h2>
        <div class="文首">
          <div class="item" v-for="(value, key) in casea.全文.文首" :key="key">
            <b><span v-html="key" />： </b> <span v-html="value" />
          </div>
        </div>
        <template v-for="(value, key) in casea.全文" :key="key">
          <div v-if="(key as unknown as string) != '文首'">
            <h3><span v-html="key" /></h3>
            <span v-html="value" />
          </div>
        </template>
        <div
          class="additional"
          v-if="
            Object.keys(casea).find((key) => key.startsWith('自定义')) !=
            undefined
          "
        >
          <template v-for="(value, key) in casea" :key="key">
            <div v-if="(key as unknown as string).startsWith('自定义')">
              <h3>
                <span
                  v-html="(key as unknown as string).split('_')[(key as unknown as string).split('_').length - 1]"
                />
              </h3>
              <span v-html="value" />
            </div>
          </template>
        </div>
      </div>
      <div class="sidebar"></div>
    </div>
  </div>
</template>

<style scoped lang="scss">
:deep(.searchbar) {
  width: 65vh;
}

.body {
  display: grid;
  grid-template-columns: 3fr 1fr;
  margin-bottom: 3rem;
}
.content {
  padding: 1rem 2rem;
  margin: 0rem 1rem;
  color: var(--text-color);
  line-height: 2;

  :deep(em) {
    font-style: normal;
    background-color: rgb(255, 222, 180);
    padding: 3px 3px;
    margin: 1px;
    border-radius: 5px;
  }
}

.文首 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  background-color: #fafafa;
  border-radius: 10px;
  padding: 1rem;
  .item {
    padding: 0.1rem;
  }
}

.additional {
  padding: 0.3rem 1rem 1rem 1.5rem;
  margin-top: 2rem;
  border-radius: 10px;
  background-color: #fafafa;
  border-color: #71aaff;
  border-width: 0 0 0 5px;
  border-style: solid;
}
</style>
