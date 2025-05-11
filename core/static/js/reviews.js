//Код для реализации интерактивного выбора
// Обработка клика по звездочке
document.querySelectorAll('.star-rating i').forEach(star => {
    star.addEventListener('click', function() {
        const rating = this.getAttribute('data-rating');
        document.getElementById('rating').value = rating;
        // Обновление внешнего вида звездочек
        updateStars(rating);
    });
});

// Функция обновления отображения звездочек
function updateStars(rating) {
    document.querySelectorAll('.star-rating i').forEach(star => {
        const starValue = star.getAttribute('data-rating');
        if (starValue <= rating) {
            star.classList.remove('bi-star');
            star.classList.add('bi-star-fill');
        } else {
            star.classList.remove('bi-star-fill');
            star.classList.add('bi-star');
        }
    });
}

// Код для подгрузки информации о мастере при его выборе
document.getElementById('id_master').addEventListener('change', function() {
    const masterId = this.value;
    if (masterId) {
        fetch(`/api/master-info/?master_id=${masterId}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayMasterInfo(data.master);
            } else {
                console.error('Ошибка:', data.error);
            }
        })
        .catch(error => console.error('Ошибка загрузки данных:', error));
    }
});

function displayMasterInfo(master) {
    const infoDiv = document.getElementById('master-info');
    if (!infoDiv) return;
    
    // Очищаем предыдущую информацию
    infoDiv.innerHTML = '';
    
    // Создаем элементы с информацией о мастере
    const card = document.createElement('div');
    card.className = 'card mt-3';
    
    // Добавляем фото, если оно есть
    if (master.photo) {
        const img = document.createElement('img');
        img.src = master.photo;
        img.className = 'card-img-top';
        img.alt = master.name;
        card.appendChild(img);
    }
    
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    
    const title = document.createElement('h5');
    title.className = 'card-title';
    title.textContent = master.name;
    
    const experience = document.createElement('p');
    experience.className = 'card-text';
    experience.textContent = `Опыт работы: ${master.experience} лет`;
    
    cardBody.appendChild(title);
    cardBody.appendChild(experience);
    card.appendChild(cardBody);
    
    infoDiv.appendChild(card);
}

// Клиентская валидация полей формы перед отправкой
function validateReviewForm() {
    let isValid = true;
    
    // Проверка имени клиента
    const nameField = document.getElementById('id_client_name');
    if (!nameField.value.trim()) {
        showError(nameField, 'Пожалуйста, укажите ваше имя');
        isValid = false;
    } else {
        clearError(nameField);
    }
    
    // Проверка текста отзыва
    const textField = document.getElementById('id_text');
    if (!textField.value.trim()) {
        showError(textField, 'Пожалуйста, напишите текст отзыва');
        isValid = false;
    } else {
        clearError(textField);
    }
    
    // Проверка рейтинга
    const ratingField = document.getElementById('rating');
    if (!ratingField.value) {
        showError(document.querySelector('.star-rating'), 'Пожалуйста, поставьте оценку');
        isValid = false;
    } else {
        clearError(document.querySelector('.star-rating'));
    }
    
    // Проверка выбора мастера
    const masterField = document.getElementById('id_master');
    if (!masterField.value) {
        showError(masterField, 'Пожалуйста, выберите мастера');
        isValid = false;
    } else {
        clearError(masterField);
    }
    
    return isValid;
}

// Вспомогательные функции
function showError(element, message) {
    // Очищаем предыдущую ошибку
    clearError(element);
    
    // Создаем элемент с сообщением об ошибке
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    // Добавляем класс is-invalid к элементу
    element.classList.add('is-invalid');
    
    // Вставляем сообщение об ошибке после элемента
    element.parentNode.appendChild(errorDiv);
}

function clearError(element) {
    // Удаляем класс is-invalid
    element.classList.remove('is-invalid');
    
    // Находим и удаляем сообщение об ошибке
    const errorDiv = element.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Подключение валидации к форме
document.getElementById('review-form').addEventListener('submit', function(event) {
    if (!validateReviewForm()) {
        event.preventDefault();
    }
});