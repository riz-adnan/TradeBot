/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['encrypted-tbn0.gstatic.com'],
    },
    webpack(config) {
        config.module.rules.push({
            test: /\.(gltf|glb)$/,
            use: {
                loader: 'file-loader',
            }
        });
        return config;
    }
}

module.exports = nextConfig
