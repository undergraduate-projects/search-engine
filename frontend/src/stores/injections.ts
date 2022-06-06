import type { InjectionKey } from 'vue';

export const updateQueryKey = Symbol() as InjectionKey<() => void>;
