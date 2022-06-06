import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';

type SearchResponseItem = {
  id: string;
  source: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    [key: string]: any;
  };
  highlight?: {
    [key: string]: string[];
  };
};
type SearchResponse = {
  total: number;
  size: number;
  offset: number;
  data: SearchResponseItem[];
};

type Query =
  | {
      type: 'keyword';
      keyword: string;
    }
  | {
      type: 'file';
      content: string;
      filename: string;
    };

export const useSearchStore = defineStore(
  'search',
  () => {
    const query = ref<Query>({
      type: 'keyword',
      keyword: '',
    });
    const resetQuery = () => {
      query.value = {
        type: 'keyword',
        keyword: '',
      };
    };

    const result = ref<SearchResponse>({
      total: 0,
      size: 0,
      offset: 0,
      data: [],
    });
    const resetResult = () => {
      result.value = {
        total: 0,
        size: 0,
        offset: 0,
        data: [],
      };
    };

    // eslint-disable-next-line vue/return-in-computed-property
    const searchBarDisplay = computed(() => {
      switch (query.value.type) {
        case 'keyword':
          return query.value.keyword;
        case 'file':
          return query.value.filename;
      }
    });

    return { query, resetQuery, result, resetResult, searchBarDisplay };
  },
  {
    persist: {
      afterRestore: (context) => {
        const route = useRoute();
        if (route.name == 'home') {
          context.store.resetQuery();
          context.store.resetResult();
        }
      },
    },
  }
);
