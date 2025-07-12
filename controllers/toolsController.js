// controllers/toolsController.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// __dirname uyarlaması
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const getAllTools = (req, res) => {
  const dataPath = path.join(__dirname, '../data/tools.json');

  fs.readFile(dataPath, 'utf8', (err, data) => {
    if (err) {
      console.error('Veri okunamadı:', err);
      return res.status(500).json({ error: 'Veri okunamadı' });
    }

    const tools = JSON.parse(data);
    res.json(tools);
  });
};

// controllers/toolsController.js'e ekle
export const getToolByName = (req, res) => {
  const toolName = req.params.toolName.toLowerCase();
  const dataPath = path.join(__dirname, '../data/tools.json');

  fs.readFile(dataPath, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Veri okunamadı' });

    const tools = JSON.parse(data);
    const foundTool = tools.find(t => t.tool.toLowerCase() === toolName);

    if (!foundTool) return res.status(404).json({ error: 'Tool bulunamadı' });

    res.json(foundTool);
  });
};

