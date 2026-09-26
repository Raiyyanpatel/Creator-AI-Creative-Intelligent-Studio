export const storage = {
  save<T>(key: string, data: T): void {
    try {
      localStorage.setItem(`creator_ai_${key}`, JSON.stringify(data));
    } catch (e) {
      console.warn('LocalStorage save failed:', e);
    }
  },

  load<T>(key: string, fallback: T): T {
    try {
      const item = localStorage.getItem(`creator_ai_${key}`);
      return item ? JSON.parse(item) : fallback;
    } catch (e) {
      console.warn('LocalStorage load failed:', e);
      return fallback;
    }
  },

  remove(key: string): void {
    try {
      localStorage.removeItem(`creator_ai_${key}`);
    } catch (e) {
      console.warn('LocalStorage remove failed:', e);
    }
  }
};
