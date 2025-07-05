const { app, BrowserWindow } = require('electron');
const path = require('path');

// Disable hardware acceleration for better compatibility with some systems
app.disableHardwareAcceleration();

// Function to create the main application window
function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, 'public', 'bot.png')
  });

  win.loadFile('index.html');
}

// This method will be called when Electron has finished
app.whenReady().then(() => {
  createWindow();

  // MacOS specific behavior
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});