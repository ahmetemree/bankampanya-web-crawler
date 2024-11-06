// ... mevcut kod ...
const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3002;

// API uç noktası
app.get('/kampanyalar', (req, res) => {
    exec('py main.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Hata: ${error.message}`);
            return res.status(500).json({ error: 'Bir hata oluştu' });
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).json({ error: 'Bir hata oluştu' });
        }
        // JSON verisini döndür
        res.json(JSON.parse(stdout));
    });
});

// Sunucuyu başlat
app.listen(port, () => {
    console.log(`Sunucu http://localhost:${port} adresinde çalışıyor`);
});