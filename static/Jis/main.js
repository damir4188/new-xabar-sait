document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var articleId = this.dataset.id;
            var csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
            if (!csrfToken) return;
            fetch('/article/' + articleId + '/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken[1],
                    'Content-Type': 'application/json',
                },
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                btn.classList.toggle('liked', data.liked);
                var countEl = btn.querySelector('.like-count');
                if (countEl) countEl.textContent = data.count;
            });
        });
    });
});