import { Ref } from 'vue';

export interface DarkModeStore {
  isEnabled: Ref<boolean>;
  isInProgress: Ref<boolean>;
  set: (payload?: boolean | null) => void;
}

export declare const useDarkModeStore: () => DarkModeStore;
