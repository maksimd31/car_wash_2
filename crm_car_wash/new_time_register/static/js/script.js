document.addEventListener('click', function () {
    const image = document.getElementById('moving-image');
    const sound = document.getElementById('sound');

    // Генерируем случайные координаты
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    const randomX = Math.random() * windowWidth;
    const randomY = Math.random() * windowHeight;

    // Устанавливаем позицию изображения
    image.style.left = `${randomX}px`;
    image.style.top = `${randomY}px`;
    image.style.display = 'block'; // Показываем изображение

    // Воспроизводим звук
    sound.currentTime = 0; // Сбрасываем время воспроизведения
    sound.play().catch(error => {
        console.error('Error playing sound:', error);
    });

    // Скрываем изображение через 1 секунду
    setTimeout(() => {
        image.style.display = 'none';
    }, 1000);
});
