/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://fleetlink-backend-rvnz.onrender.com/:path*',
      },
    ]
  },
}

module.exports = nextConfig