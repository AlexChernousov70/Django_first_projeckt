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