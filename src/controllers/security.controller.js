import { detectPhishingText, detectMaliciousContent } from "../detectors/phishing.detector.js";
import { anonymizePII } from "../pii/anonymizer.js";
import { saveThreat, getAllThreats } from "../models/threat.model.js";

export const detectPhishing = async (req, res) => {
  const { text } = req.body;

  if (!text) return res.status(400).json({ error: "Debe enviar un campo 'text'" });

  const phishingDetected = detectPhishingText(text);
  const maliciousDetected = detectMaliciousContent(text);

  if (phishingDetected.length > 0 || maliciousDetected.length > 0) {
    saveThreat({
      type: "PHISHING",
      details: { phishingDetected, maliciousDetected },
      timestamp: new Date()
    });
  }

  res.json({
    phishingDetected,
    maliciousDetected
  });
};

export const anonymizeData = async (req, res) => {
  const { text } = req.body;

  if (!text) return res.status(400).json({ error: "Debe enviar un campo 'text'" });

  const result = anonymizePII(text);

  res.json({
    original: text,
    anonymized: result
  });
};

export const getThreats = async (req, res) => {
  const threats = getAllThreats();
  res.json({ threats });
};
