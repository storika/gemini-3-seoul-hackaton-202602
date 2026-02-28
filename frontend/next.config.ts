import type { NextConfig } from "next";

const API_URL = process.env.API_URL || "http://localhost:8001";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: `${API_URL}/api/:path*` },
      { source: "/images/:path*", destination: `${API_URL}/images/:path*` },
      { source: "/videos/:path*", destination: `${API_URL}/videos/:path*` },
    ];
  },
};

export default nextConfig;
