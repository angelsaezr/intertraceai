const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('api', {
  saludar: () => {
    return '¡Hola desde el preload!';
  }
});