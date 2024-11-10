const path = require('path');

module.exports = {
  entry: './docs/index.js',  // Путь к вашему исходному файлу в папке docs
  output: {
    filename: 'main.js',  // Название выходного файла
    path: path.resolve(__dirname, 'docs'),  // Папка для выходных файлов
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,  // Преобразуем .js и .jsx файлы
        exclude: /node_modules/,
        use: 'babel-loader',  // Используем Babel для транспиляции
      },
      {
        test: /\.css$/,  // Стили
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Разрешаем .js и .jsx файлы
  },
  devServer: {
    static: path.resolve(__dirname, 'docs'),  // Статика из папки docs
    port: 8000,  // Порт для сервера
  },
  mode: 'development',  // Режим разработки
};