// routes/toolsRoutes.js
import { apiKeyAuth } from "../middleware/apiKeyAuth.js";
import express from "express";
import { getAllTools, getToolByName } from "../controllers/toolsController.js";

const router = express.Router();

router.get('/', apiKeyAuth, getAllTools);
router.get('/:toolName', apiKeyAuth, getToolByName);

export default router;
