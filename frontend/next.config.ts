import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/api/:path*", destination: "http://localhost:8001/api/:path*" },
      { source: "/images/:path*", destination: "http://localhost:8001/images/:path*" },
      { source: "/videos/:path*", destination: "http://localhost:8001/videos/:path*" },
    ];
  },
};

export default nextConfig;
