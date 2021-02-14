const { app, BrowserWindow, Menu } = require('electron')
const path = require('path')
const url = require('url')
const shell = require('electron').shell

function createWindow () {
  const win = new BrowserWindow({
    width: 1679,
    height: 871,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('index.html')

//   var menu = Menu.buildFromTemplate([
//       {
//           label: 'Menu',
//           sumbenu: [
//               {label: 'Adjust Notification Value'},
//               {label: 'CoinMarketCap'},
//               {label: 'Exit'}
//           ]
//       }
//   ])
//   Menu.setApplicationMenu(menu);
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
