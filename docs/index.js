import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';  // Импортируем из 'react-dom/client'
import { motion } from 'framer-motion';
import './style.css'; // Ваши стили

// Функция для получения данных пользователя
const fetchUserData = async (userId) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/user/${userId}`);
    if (!response.ok) {
      throw new Error('Ошибка сети');
    }
    return await response.json();
  } catch (error) {
    console.error('Ошибка:', error);
    return { full_name: "Не удалось загрузить имя.", balance: "Не удалось загрузить баланс." };
  }
};

const App = () => {
  const [currentPage, setCurrentPage] = useState('main'); // Страница, на которой мы находимся
  const [userData, setUserData] = useState({ full_name: '', balance: '' });

  // Инициализация данных пользователя
  useEffect(() => {
    if (currentPage === 'profile') {
      // Проверяем, что приложение работает в WebView Telegram
      if (window.Telegram && window.Telegram.WebApp) {
        const tg = window.Telegram.WebApp;

        // Проверка на доступность данных
        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
          const userId = tg.initDataUnsafe.user.id;

          fetchUserData(userId).then((data) => {
            setUserData(data);
          }).catch(error => {
            console.error("Ошибка при загрузке данных пользователя:", error);
          });
        } else {
          console.error("Не удалось найти данные пользователя в WebApp.");
        }
      } else {
        console.log("Приложение не запущено в Telegram WebView.");
      }
    }
  }, [currentPage]);

  return (
    <div>
      {/* Основной контент */}
      {currentPage === 'main' && (
        <div id="mainContent">
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
          >
            English Nova
          </motion.h1>
          <motion.button
            onClick={() => setCurrentPage('profile')}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 1 }}
          >
            Профиль
          </motion.button>
          <motion.button
            onClick={() => setCurrentPage('start_learning')}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 1 }}
          >
            Начать обучение
          </motion.button>
        </div>
      )}

      {/* Профиль пользователя */}
      {currentPage === 'profile' && (
        <div id="profileContent">
          <h2>Профиль пользователя</h2>
          <p id="full_name">Имя пользователя: {userData.full_name}</p>
          <p id="balance">Баланс: {userData.balance}</p>
          <button onClick={() => setCurrentPage('main')}>Назад</button>
        </div>
      )}

      {/* Начало обучения */}
      {currentPage === 'start_learning' && (
        <div id="start_learning_context">
          <h2>Начало обучения</h2>
          <button onClick={() => alert('Вы выбрали Времена')}>Времена</button>
          <button onClick={() => alert('Вы выбрали Неправильные глаголы')}>Неправильные глаголы</button>
          <button onClick={() => setCurrentPage('main')}>Назад</button>
        </div>
      )}
    </div>
  );
};

// Рендерим приложение с использованием createRoot
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
