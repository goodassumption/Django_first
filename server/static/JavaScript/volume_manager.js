document.addEventListener('DOMContentLoaded', function() {
    const video = document.getElementById('customVideo');
    const volumeSlider = document.getElementById('volumeSlider');
    const volumeValue = document.getElementById('volumeValue');
    const muteBtn = document.getElementById('muteBtn');
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const sliderProgress = document.querySelector('.slider-progress');
    const videoWrapper = document.getElementById('videoWrapper');
    const answerText = document.getElementById('answerText');
    
    // Флаг для отслеживания состояния видео
    let isVideoVisible = false;
    let hasPlayedOnce = false;
    
    // Обработчик клика на answerText
    answerText.addEventListener('click', function() {
        if (!isVideoVisible) {
            // Показываем видео
            videoWrapper.style.display = 'block';
            isVideoVisible = true;
            
            // Если видео еще не проигрывалось или нужно проиграть снова
            if (!hasPlayedOnce) {
                // Запускаем видео
                video.play().then(() => {
                    hasPlayedOnce = true;
                }).catch(error => {
                    console.error('Ошибка воспроизведения видео:', error);
                    alert('Не удалось воспроизвести видео. Проверьте поддержку формата браузером.');
                });
            }
        } else {
            // Скрываем видео
            videoWrapper.style.display = 'none';
            isVideoVisible = false;
            
            // Останавливаем видео и сбрасываем время
            video.pause();
            video.currentTime = 0;
        }
    });
    
    // Обработчик завершения видео
    video.addEventListener('ended', function() {
        // После окончания воспроизведения останавливаем видео
        video.pause();
        // Сбрасываем время воспроизведения в начало
        video.currentTime = 0;
        // Сбрасываем флаг, чтобы при следующем показе видео снова проигралось
        hasPlayedOnce = false;
    });
    
    // Настройка громкости через ползунок
    volumeSlider.addEventListener('input', function() {
        const volume = parseFloat(this.value);
        video.volume = volume;
        
        // Обновление отображения
        updateVolumeDisplay(volume);
        
        // Анимация изменения
        volumeSlider.classList.add('volume-changing');
        setTimeout(() => {
            volumeSlider.classList.remove('volume-changing');
        }, 300);
    });
    
    // Обновление отображения громкости
    function updateVolumeDisplay(volume) {
        const percent = Math.round(volume * 100);
        volumeValue.textContent = percent + '%';
        volumeValue.style.color = volume === 0 ? '#f46b45' : '#3a7bd5';
        
        // Обновление прогресса ползунка
        sliderProgress.style.transform = `translateY(-50%) scaleX(${volume})`;
        
        // Обновление иконки
        const volumeIcon = document.querySelector('.volume-icon');
        if (volume === 0) {
            volumeIcon.textContent = '🔇';
        } else if (volume < 0.3) {
            volumeIcon.textContent = '🔈';
        } else if (volume < 0.7) {
            volumeIcon.textContent = '🔉';
        } else {
            volumeIcon.textContent = '🔊';
        }
    }
    
    // Кнопка отключения звука
    muteBtn.addEventListener('click', function() {
        if (video.volume > 0) {
            video.dataset.previousVolume = video.volume;
            video.volume = 0;
            volumeSlider.value = 0;
        } else {
            const previousVolume = parseFloat(video.dataset.previousVolume || 0.5);
            video.volume = previousVolume;
            volumeSlider.value = previousVolume;
        }
        updateVolumeDisplay(video.volume);
    });
    
    // Кнопка полного экрана
    fullscreenBtn.addEventListener('click', function() {
        if (!document.fullscreenElement) {
            if (video.requestFullscreen) {
                video.requestFullscreen();
            } else if (video.webkitRequestFullscreen) {
                video.webkitRequestFullscreen();
            } else if (video.msRequestFullscreen) {
                video.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    });
    
    // Кнопка скачивания
    downloadBtn.addEventListener('click', function() {
        const videoSrc = video.querySelector('source').src;
        const link = document.createElement('a');
        link.href = videoSrc;
        link.download = 'video_' + new Date().getTime() + '.mp4';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    // Синхронизация громкости при изменении видео
    video.addEventListener('volumechange', function() {
        volumeSlider.value = video.volume;
        updateVolumeDisplay(video.volume);
    });
    
    // Инициализация
    updateVolumeDisplay(video.volume);
    
    // Обработка ошибок загрузки видео
    video.addEventListener('error', function() {
        console.error('Ошибка загрузки видео');
        alert('Не удалось загрузить видеофайл. Проверьте путь к файлу.');
    });
    
    // Индикатор загрузки
    video.addEventListener('waiting', function() {
        console.log('Видео загружается...');
    });
    
    video.addEventListener('canplay', function() {
        console.log('Видео готово к воспроизведению');
    });
    
    // Управление с клавиатуры
    document.addEventListener('keydown', function(e) {
        // Проверяем, видно ли видео
        if (videoWrapper.style.display === 'none') {
            return;
        }
        
        switch(e.key) {
            case ' ':
                e.preventDefault();
                video.paused ? video.play() : video.pause();
                break;
            case 'ArrowUp':
                e.preventDefault();
                video.volume = Math.min(1, video.volume + 0.1);
                volumeSlider.value = video.volume;
                updateVolumeDisplay(video.volume);
                break;
            case 'ArrowDown':
                e.preventDefault();
                video.volume = Math.max(0, video.volume - 0.1);
                volumeSlider.value = video.volume;
                updateVolumeDisplay(video.volume);
                break;
            case 'm':
            case 'M':
                e.preventDefault();
                video.muted = !video.muted;
                break;
        }
    });
});