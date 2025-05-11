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
// Клиентская валидация полей формы перед отправкой