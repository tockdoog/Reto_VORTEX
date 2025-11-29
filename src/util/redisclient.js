import { createClient } from "redis";

export const redis = createClient({
  url: process.env.REDIS_URL || "redis://localhost:6379"
});

redis.on("connect", () => console.log("Redis conectado MS-Security-Service"));
redis.on("error", (err) => console.error("Redis error:", err));

redis.connect();
