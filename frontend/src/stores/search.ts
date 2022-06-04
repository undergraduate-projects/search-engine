import { defineStore } from 'pinia';
import { ref } from 'vue';

type SearchResponseItem = {
  id: string;
  source: {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    [key: string]: any;
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

export const useSearchStore = defineStore('search', () => {
  const query = ref('');

  const resultEmpty = {
    total: 0,
    size: 0,
    offset: '',
    data: [],
  };
  const result = ref<SearchResponse>(resultEmpty);
  const resetResult = () => {
    result.value = resultEmpty;
  };

  return { query, resetResult, result };
});
