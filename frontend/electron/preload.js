import { contextBridge } from 'electron';

// Expose API to the renderer process
contextBridge.exposeInMainWorld('api', {
  saludar: () => {
    return '¡Hola desde el preload!';
  }
});