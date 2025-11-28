// src/utils/internal-call.js
import jwt from "jsonwebtoken";
import axios from "axios";
import dotenv from "dotenv";
dotenv.config();

export const callInternalService = async (url, method = "GET", data = null) => {
  const internalToken = jwt.sign(
    { from: "gateway", ts: Date.now() },
    process.env.INTERNAL_SECRET,
    { expiresIn: "10m" }
  );

  const headers = {
    Authorization: `Bearer ${internalToken}`,
    "Content-Type": "application/json"
  };

   const config = { url, method, headers };

  if (method !== "GET" && data !== null) {
    config.data = data;
  }

  return axios(config);
};
