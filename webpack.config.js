const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');  // Плагин для генерации HTML

module.exports = {
  entry: './docs/index.js',  // Путь к вашему исходному файлу в папке docs
  output: {
    filename: 'main.js',  // Название выходного файла
    path: path.resolve(__dirname, 'docs'),  // Папка для выходных файлов (docs)
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,  // Преобразуем .js и .jsx файлы
        exclude: /node_modules/,
        use: 'babel-loader',  // Используем Babel для транспиляции
      },
      {
        test: /\.css$/,  // Преобразуем CSS файлы
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Разрешаем .js и .jsx файлы
  },
  devServer: {
    static: path.resolve(__dirname, 'docs'),  // Папка с результатами сборки (docs)
    port: 8000,  // Порт для сервера
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './docs/index.html',  // Путь к вашему шаблону HTML в папке docs
      filename: 'index.html',  // Генерируем файл index.html в выходной папке (docs)
    }),
  ],
  mode: 'development',  // Режим разработки
};