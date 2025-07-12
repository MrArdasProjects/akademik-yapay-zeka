// routes/chat.js
import express from 'express';
import { chatResponse } from '../controllers/chatController.js';
import { apiKeyAuth } from '../middleware/apiKeyAuth.js';

const router = express.Router();

router.post('/', apiKeyAuth, chatResponse);

export default router;
