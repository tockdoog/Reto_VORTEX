import { Router } from "express";
import {
  detectPhishing,
  anonymizeData,
  getThreats
} from "../controllers/security.controller.js";

const router = Router();

router.post("/detect-phishing", detectPhishing);
router.post("/anonymize-data", anonymizeData);
router.get("/threats", getThreats);

export default router;
