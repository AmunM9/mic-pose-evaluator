/** @type {import('next').NextConfig} */
const nextConfig = {
  ...(process.env.NEXT_STANDALONE === "1" ? { output: "standalone" } : {}),
};

module.exports = nextConfig;
