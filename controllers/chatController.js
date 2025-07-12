// controllers/chatController.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const chatResponse = async (req, res) => {
  const userMessage = req.body.message;

  if (!userMessage) {
    return res.status(400).json({ error: 'Mesaj eksik' });
  }

  try {
    // Python servise POST isteği gönder
    const response = await axios.post('http://localhost:5000/api/rag', {
      query: userMessage
    });

    const suggestedToolName = response.data.tool?.toLowerCase();

    // tools.json'dan tool'u bul
    const dataPath = path.join(__dirname, '../data/tools.json');
    const tools = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
    const matchedTool = tools.find(t => t.tool.toLowerCase() === suggestedToolName);

    if (!matchedTool) {
      return res.status(404).json({ error: 'Önerilen araç bulunamadı' });
    }

    res.json(matchedTool);

  } catch (err) {
    console.error('RAG API hatası:', err.message);
    res.status(500).json({ error: 'RAG sistemine bağlanılamadı' });
  }
};
