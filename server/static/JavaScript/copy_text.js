// Основная функция копирования
async function copyTextOnClick(element) {
    // Определяем, какой текст копировать
    // Приоритет 1: data-copy-text атрибут
    // Приоритет 2: textContent элемента (без иконки)
    let textToCopy = element.getAttribute('data-copy-text');
    
    if (!textToCopy) {
        // Удаляем иконку копирования из текста
        const tempElement = element.cloneNode(true);
        const icons = tempElement.querySelectorAll('.copy-icon');
        icons.forEach(icon => icon.remove());
        textToCopy = tempElement.textContent.trim();
    }

    // Получаем дополнительную информацию (если есть)
    const metaInfo = element.getAttribute('data-copy-meta') || 'Текст';

    try {
        // Пробуем использовать современный Clipboard API
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(textToCopy);
            showCopySuccess(element, textToCopy, metaInfo);
        } else {
            // Fallback для старых браузеров или HTTP
            copyUsingFallback(textToCopy, element, metaInfo);
        }
    } catch (err) {
        console.error('Ошибка при копировании:', err);
        // Второй fallback, если и первый не сработал
        copyUsingFallback(textToCopy, element, metaInfo);
    }
}

// Fallback метод для старых браузеров
function copyUsingFallback(text, element, metaInfo) {
    // Создаем временный textarea
    const textArea = document.createElement('textarea');
    textArea.value = text;
    
    // Стили, чтобы элемент не был виден
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    textArea.style.opacity = '0';
    textArea.style.pointerEvents = 'none';
    
    document.body.appendChild(textArea);
    
    try {
        // Выделяем и копируем
        textArea.select();
        textArea.setSelectionRange(0, 99999); // Для мобильных устройств
        
        // Пробуем скопировать
        const successful = document.execCommand('copy');
        
        if (successful) {
            showCopySuccess(element, text, metaInfo);
        } else {
            throw new Error('Не удалось выполнить команду copy');
        }
    } catch (err) {
        console.error('Fallback копирование не удалось:', err);
        showCopyError(element);
    } finally {
        // Удаляем временный элемент
        document.body.removeChild(textArea);
    }
}

// Показать успешное копирование через алерт
function showCopySuccess(element, copiedText, metaInfo) {
    // 1. Визуальная обратная связь на элементе
    element.classList.add('copied');
    
    // 2. Создаем алерт об успехе
    showAlert(`${metaInfo} скопирован: ${truncateText(copiedText, 30)}`, 'success');
    
    // 3. Восстановить исходное состояние элемента через 1.5 секунды
    setTimeout(() => {
        element.classList.remove('copied');
    }, 1500);
    
    // 4. Опционально: логирование в консоль
    console.log(`Скопировано: ${copiedText}`);
    
    // 5. Отправить аналитику (если нужно)
    sendCopyAnalytics(metaInfo, copiedText.length);
}

// Показать ошибку копирования через алерт
function showCopyError(element) {
    // Создаем алерт об ошибке
    showAlert('Не удалось скопировать текст', 'danger');
    
    // Мигание элемента красным
    element.style.backgroundColor = '#ffebee';
    setTimeout(() => {
        element.style.backgroundColor = '';
    }, 500);
}

// Функция для показа алертов
function showAlert(message, type = 'info') {
    // Создаем контейнер для алертов, если его нет
    let alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.id = 'alert-container';
        alertContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 400px;
            pointer-events: none;
        `;
        document.body.appendChild(alertContainer);
    }
    
    // Создаем алерт
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fade-in`;
    alert.style.cssText = `
        pointer-events: auto;
        animation: slideIn 0.3s ease-out;
        margin-bottom: 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        max-width: 400px;
        word-break: break-word;
        transition: opacity 0.3s, transform 0.3s;
    `;
    
    // Добавляем текст и кнопку закрытия
    alert.innerHTML = `
        <span>${message}</span>
        <button type="button" class="alert-close" aria-label="Закрыть" 
                style="background: none; border: none; color: inherit; cursor: pointer; 
                       margin-left: 10px; font-size: 1.2rem; line-height: 1;">
            &times;
        </button>
    `;
    
    // Добавляем алерт в контейнер
    alertContainer.appendChild(alert);
    
    // Обработчик закрытия алерта
    const closeBtn = alert.querySelector('.alert-close');
    closeBtn.addEventListener('click', () => {
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 300);
    });
    
    // Автоматическое скрытие через 2 секунды
    setTimeout(() => {
        if (alert.parentNode) {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        }
    }, 2000); // Изменено с 3000 на 2000
    
    // Отмена автоскрытия при наведении
    let autoRemoveTimer;
    alert.addEventListener('mouseenter', () => {
        // Очищаем таймер автоскрытия при наведении
        clearTimeout(autoRemoveTimer);
    });
    
    alert.addEventListener('mouseleave', () => {
        // При уходе мыши снова устанавливаем таймер на 2 секунды
        autoRemoveTimer = setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 2000); // Изменено с 1000 на 2000
    });
}

// Вспомогательная функция для обрезания текста
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Функция для отправки аналитики (заглушка)
function sendCopyAnalytics(type, length) {
    // Здесь можно отправить данные в Google Analytics, Яндекс.Метрику и т.д.
    console.log(`Аналитика: скопирован ${type}, длина: ${length} символов`);
}

// Дополнительная функциональность

// Копирование при двойном клике (альтернатива)
document.querySelectorAll('.copyable').forEach(element => {
    element.addEventListener('dblclick', function(e) {
        e.stopPropagation();
        copyTextOnClick(this);
        showAlert('Скопировано по двойному клику!', 'info');
    });
});

// Копирование по нажатию Ctrl/Cmd + клик
document.querySelectorAll('.copyable').forEach(element => {
    element.addEventListener('click', function(e) {
        if (e.ctrlKey || e.metaKey) {
            e.preventDefault(); // Предотвращаем стандартное поведение
            e.stopPropagation();
            copyTextOnClick(this);
            showAlert('Скопировано по Ctrl+клик!', 'info');
        }
    });
});

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Добавляем атрибут title для дополнительной подсказки
    document.querySelectorAll('.copyable').forEach(element => {
        if (!element.hasAttribute('title')) {
            element.setAttribute('title', 'Кликните, чтобы скопировать. Ctrl+клик для альтернативного копирования.');
        }
    });
    
    // Показываем подсказку при первом посещении
    if (!localStorage.getItem('copyHintShown')) {
        setTimeout(() => {
            showAlert('💡 Подсказка: кликайте на цветные блоки для копирования текста', 'warning');
            localStorage.setItem('copyHintShown', 'true');
        }, 1000);
    }
});

// Функция для копирования текста из любого места на странице
window.copyAnyText = function(text, metaInfo = 'Текст') {
    // Создаем временный элемент для копирования
    const tempElement = document.createElement('div');
    tempElement.className = 'copyable copyable-code';
    tempElement.textContent = text;
    document.body.appendChild(tempElement);
    
    // Вызываем функцию копирования
    copyToClipboard(text, tempElement, metaInfo);
    
    // Удаляем временный элемент
    setTimeout(() => {
        document.body.removeChild(tempElement);
    }, 2000);
};

// Универсальная функция копирования
async function copyToClipboard(text, element, metaInfo) {
    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text);
            showCopySuccess(element, text, metaInfo);
        } else {
            copyUsingFallback(text, element, metaInfo);
        }
    } catch (err) {
        console.error('Ошибка при копировании:', err);
        copyUsingFallback(text, element, metaInfo);
    }
}
