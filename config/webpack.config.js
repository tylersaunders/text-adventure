const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: {
    app: ['./web/main.ts', './web/styles.scss'],
  },
  output: {
    path: path.resolve(__dirname, '../build'),
    filename: 'bundle.js',
  },

  mode: 'development',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      //{
      // test: /\.js$/,
      // exclude: /(node_modules)/,
      // use: {
      // loader: 'babel-loader',
      // options: {
      // presets: ['@babel/preset-env'],
      //},
      //},
      //},
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            // After all CSS loaders we use plugin to do his work.
            // It gets all transformed CSS and extracts it into separate
            // single bundled file
            loader: MiniCssExtractPlugin.loader,
          },
          {
            // This loader resolves url() and @imports inside CSS
            loader: 'css-loader',
          },
          {
            // Then we apply post CSS fixes like autoprefixer and minifying
            loader: 'postcss-loader',
            options: {config: {path: 'config/postcss.config.js'}},
          },
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass'),
            },
          },
        ],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'bundle.css',
    }),
  ],
};
