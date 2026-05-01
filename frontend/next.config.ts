/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://4.187.201.97:8000/:path*',
      },
    ]
  },
}

module.exports = nextConfig