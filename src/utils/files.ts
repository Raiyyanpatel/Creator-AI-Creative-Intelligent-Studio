export interface PickedFile {
  name: string;
  size: number;
  type: string;
  url: string;
}

export const files = {
  async pick(accept = 'video/*,image/*,audio/*'): Promise<PickedFile | null> {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = accept;
      input.onchange = (e: any) => {
        const file = e.target?.files?.[0];
        if (!file) {
          resolve(null);
          return;
        }
        const url = URL.createObjectURL(file);
        resolve({
          name: file.name,
          size: file.size,
          type: file.type,
          url
        });
      };
      input.click();
    });
  },

  copy(sourcePath: string, targetPath: string): boolean {
    console.log(`Copying ${sourcePath} -> ${targetPath}`);
    return true;
  },

  delete(path: string): boolean {
    console.log(`Deleting ${path}`);
    return true;
  },

  rename(oldName: string, newName: string): string {
    return newName;
  }
};
