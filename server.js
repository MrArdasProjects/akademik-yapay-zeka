// server.js

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import toolsRoutes from './routes/tools.js';
import chatRoutes from './routes/chat.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// API Routes
app.use('/api/tools', toolsRoutes);         // → /api/tools (hepsi ve detay)

app.use('/api/chat-response', chatRoutes);    // → /api/chat-response (chatbot)

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
