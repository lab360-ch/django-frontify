const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env, options, cfg) => {
    return {
        entry: {
            widget: [
                './django_frontify/static_src/scss/frontify-widget.scss',
                './django_frontify/static_src/typescript/frontify-widget.ts'
            ]
        },
        output: {
            filename: `[name].js`,
            path: path.resolve(__dirname, `django_frontify/static/django_frontify/`)
            // publicPath: '/static/'
        },
        resolve: {
            extensions: [".ts", ".js"]
        },
        plugins: [new MiniCssExtractPlugin({
            // Options similar to the same options in webpackcfg.output
            // both options are optional
            filename: `[name].css`,
            //   chunkFilename: HASED_FILE_NAMES ? '[id].[hash].css' : '[id].css',
        })],

        module: {
            rules: [{
                test: /\.tsx?$/,
                use: [{
                    loader: "babel-loader"
                }, {
                    loader: 'ts-loader',
                    options: {
                        transpileOnly: true,
                        experimentalWatchApi: true,
                        configFile: options.mode === 'production' ? path.resolve(__dirname, 'tsconfig.prod.json') : path.resolve(__dirname, 'tsconfig.dev.json')
                    }
                }],
                exclude: /node_modules/,
            }, {
                test: /\.s?[ac]ss$/,
                use: [{
                    loader: MiniCssExtractPlugin.loader
                }, {
                    loader: 'css-loader',
                    options: {
                        sourceMap: true,
                    }
                }, {
                    loader: 'postcss-loader',
                    options: {
                        sourceMap: true,
                    }
                }, {
                    loader: 'sass-loader',
                    options: {
                        sourceMap: true,
                        sassOptions: {
                            includePaths: ['node_modules'],
                            outputStyle: 'compressed',
                        }
                    }
                }],
            }]
        },
    }
};