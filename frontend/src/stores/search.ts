import { defineStore } from 'pinia';
import { computed, ref } from 'vue';

type SearchResponseItem = {
  source: {
    [key: string]: unknown;
  };
  highlight: {
    [key: string]: string[];
  };
};
type SearchResponse = {
  total: number;
  size: number;
  offset: string;
  data: SearchResponseItem[];
};

type SearchResponseItemIndexed = SearchResponseItem & {
  id: number;
};
type SearchResponseIndexed = SearchResponse & {
  data: SearchResponseItemIndexed[];
};

export const useSearchStore = defineStore('search', () => {
  const query = ref('');

  const rawResultEmpty = {
    total: 0,
    size: 0,
    offset: '',
    data: [],
  };
  const rawResult = ref<SearchResponse>(rawResultEmpty);
  const setResult = (result?: SearchResponse) => {
    if (result) rawResult.value = result;
    else rawResult.value = rawResultEmpty;
  };
  const result = computed<SearchResponseIndexed>(() => ({
    ...rawResult.value,
    data: rawResult.value.data.map((item, index) => ({
      ...item,
      id: index,
    })),
  }));

  return { query, setResult, result };
});
