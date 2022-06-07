<template>
  <div class="root-searchbar">
    <form @submit="handleSubmit">
      <span class="p-input-icon-right mr-2">
        <InputText
          type="text"
          class="searchbar"
          :model-value="search.searchBarDisplay"
          @update:model-value="(newValue: string) => (queryKeyword.keyword = newValue)"
        />
        <i
          class="pi pi-folder"
          v-tooltip.bottom="'上传案例文件'"
          @click="openFileUpload"
        />
      </span>

      <Button icon="pi pi-search" type="submit" />
      <Button
        label="高级搜索"
        class="p-button-outlined ml-2"
        @click="openAdvancedSearch"
      />
    </form>
    <template v-if="showAdvancedSearch">
      <div class="advanced">
        <div class="field">
          <label>案件类别</label>
          <MultiSelect
            v-model="queryKeyword.AJLB"
            :options="[
              '行政案件',
              '刑罚变更案件',
              '民事案件',
              '执行案件',
              '刑事案件',
              '赔偿案件',
            ]"
          />
        </div>
        <div class="field">
          <label>审判程序</label>
          <MultiSelect
            v-model="queryKeyword.SPCX"
            :options="[
              '特别程序案件',
              '刑罚变更案件',
              '复核案件',
              '二审案件',
              '强制医疗案件',
              '再审复查与审判监督案件',
              '再审案件',
              '破产案件',
              '非诉执行审查案件',
              '一审案件',
            ]"
          />
        </div>
        <div class="field">
          <label>法官成员</label>
          <Chips v-model="queryKeyword.FGCY" separator="," />
        </div>
        <div class="field">
          <label>案号</label>
          <InputText type="text" v-model="queryKeyword.AH" />
        </div>
        <div class="field">
          <label>案由</label>
          <InputText type="text" v-model="queryKeyword.AY" />
        </div>
        <div class="field">
          <label>经办法院</label>
          <InputText type="text" v-model="queryKeyword.JBFY" />
        </div>
        <div class="field">
          <label>文书种类</label>
          <MultiSelect
            v-model="queryKeyword.WSZL"
            :options="[
              '调解书',
              '不起诉书',
              '起诉书',
              '应诉通知书',
              '裁定书',
              '决定书',
              '判决书',
              '起诉状',
              '暂予监外执行案例',
            ]"
          />
        </div>
      </div>
    </template>
    <OverlayPanel ref="fileUpload" :showCloseIcon="true">
      <FileUpload
        :custom-upload="true"
        @uploader="fileUploader"
        :file-limit="1"
        accept=".xml"
      >
        <template #empty>
          <p>Drag and drop files to here to upload.</p>
        </template>
      </FileUpload>
    </OverlayPanel>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import OverlayPanel from 'primevue/overlaypanel';
import FileUpload from 'primevue/fileupload';
import type { FileUploadUploaderEvent } from 'primevue/fileupload';
import MultiSelect from 'primevue/multiselect';
import Chips from 'primevue/chips';
import { type QueryKeyword, useSearchStore } from '@/stores/search';
import { inject, ref } from 'vue';
import { updateQueryKey } from '@/stores/injections';

defineProps<{
  withButton: boolean;
}>();

const router = useRouter();
const search = useSearchStore();

const queryKeyword = ref<Omit<QueryKeyword, 'type'>>({
  ...(search.query.type == 'keyword' ? search.query : {}),
  keyword: search.searchBarDisplay,
});

const showAdvancedSearch = ref(
  search.query.type == 'keyword' &&
    ((search.query.AJLB && search.query.AJLB.length > 0) ||
      (search.query.SPCX && search.query.SPCX.length > 0) ||
      (search.query.FGCY && search.query.FGCY.length > 0) ||
      search.query.AH ||
      search.query.AY ||
      search.query.JBFY ||
      search.query.WSZL)
);

const fileUpload = ref();

const updateQuery = inject(updateQueryKey);
function query() {
  search.resetResult();
  router.push({
    name: 'search',
  });
  updateQuery?.();
}

const handleSubmit = (e: Event) => {
  e.preventDefault();
  if (!queryKeyword.value.keyword) return;

  if (!showAdvancedSearch.value)
    queryKeyword.value = { keyword: queryKeyword.value.keyword };
  search.query = {
    ...queryKeyword.value,
    type: 'keyword',
  };
  query();
};

const openFileUpload = (event: Event) => {
  let newEvent = Object.assign(event);
  fileUpload.value.toggle(newEvent);
};

const fileUploader = (event: FileUploadUploaderEvent) => {
  let fileReader = new FileReader();
  fileReader.onload = () => {
    fileUpload.value.hide();
    search.query = {
      type: 'file',
      content: fileReader.result as string,
      filename: (event.files as File[])[0].name,
    };
    showAdvancedSearch.value = false;
    query();
  };
  fileReader.readAsText((event.files as File[])[0]);
};

function openAdvancedSearch() {
  showAdvancedSearch.value = !showAdvancedSearch.value;
}
</script>

<style scoped lang="scss">
.pi-folder {
  cursor: pointer;
}

.advanced {
  margin: 1.5rem 2rem 0.5rem 0em;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  column-gap: 1rem;
  row-gap: 0.8rem;
  color: var(--text-color);
  // width: 60vw;
  .field {
    display: flex;
    flex-direction: column;
    margin: 0;
    min-width: 0;
  }
  label {
    margin: 0 0 0.5rem 0.3rem;
  }

  :deep(.p-chips-multiple-container) {
    flex-grow: 1;
  }
}
</style>
