<template>
  <form v-if="withButton" @submit="handleSubmit">
    <span class="p-input-icon-right mr-2">
      <InputText type="text" v-model="searchQuery" class="searchbar" />
      <i
        class="pi pi-folder"
        v-tooltip.bottom="'上传案例文件'"
        @click="openFileUpload"
      />
    </span>

    <Button icon="pi pi-search" type="submit" />
  </form>
  <form v-else @submit="handleSubmit">
    <span class="p-input-icon-left p-input-icon-right">
      <i class="pi pi-search" />
      <InputText
        ref="inputtext"
        type="text"
        v-model="searchQuery"
        class="searchbar"
        placeholder="Search"
      />
      <i
        class="pi pi-folder"
        v-tooltip.bottom="'上传案例文件'"
        @click="openFileUpload"
      />
    </span>
  </form>
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
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import OverlayPanel from 'primevue/overlaypanel';
import FileUpload from 'primevue/fileupload';
import type { FileUploadUploaderEvent } from 'primevue/fileupload';
import { useSearchStore } from '@/stores/search';
import { ref } from 'vue';

defineProps<{
  withButton: boolean;
}>();

const router = useRouter();
const search = useSearchStore();
const searchQuery = ref(
  (() => {
    switch (search.query.type) {
      case 'keyword':
        return search.query.keyword;
      case 'file':
        return search.query.filename;
    }
  })()
);
const fileUpload = ref();

const emit = defineEmits<{
  (e: 'submit'): void;
}>();

const handleSubmit = (e: Event) => {
  e.preventDefault();
  if (!searchQuery.value) return;
  search.query = {
    type: 'keyword',
    keyword: searchQuery.value,
  };
  search.resetResult();
  router.push({
    name: 'search',
  });
  emit('submit');
};

const openFileUpload = (event: Event) => {
  let newEvent = Object.assign(event);
  fileUpload.value.toggle(newEvent);
};

const fileUploader = (event: FileUploadUploaderEvent) => {
  let fileReader = new FileReader();
  fileReader.onload = () => {
    search.query = {
      type: 'file',
      content: fileReader.result as string,
      filename: (event.files as File[])[0].name,
    };
    search.resetResult();
    router.push({
      name: 'search',
    });
    emit('submit');
  };
  fileReader.readAsText((event.files as File[])[0]);
};
</script>

<style scoped lang="scss">
.pi-folder {
  cursor: pointer;
}
</style>
