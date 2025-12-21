document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('search_form');
    const resultsDiv = document.getElementById('results');
    const submitBtn = form.querySelector('button[type="submit"]');

    let isSearching = false;
    // Template centralizado de carregamento
    const loaderHtml = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary-blue" style="width: 3rem; height: 3rem;" role="status">
                <span class="visually-hidden">Carregando...</span>
            </div>
            <p class="text-secondary mt-3 fw-medium">Carregando consertos...</p>
        </div>
    `;

    function repair_search(page = 1) {
        // Trava de segurança para evitar múltiplas requisições
        if (isSearching) return;
        isSearching = true;
        // Desabilita o botão apenas para indicar que a ação foi recebida
        submitBtn.disabled = true;
        // Injeta o loader na área de resultados
        resultsDiv.innerHTML = loaderHtml;
        resultsDiv.style.opacity = '0.8';

        const apiUrl = form.getAttribute('action');
        const formData = new FormData(form);
        const params = new URLSearchParams();
        // Converte os dados do formulário em parâmetros de URL,
        // ignorando campos vazios para manter a URL limpa e evitar filtros nulos no backend.
        for (let [key, value] of formData.entries()) {
            if (value) params.append(key, value);
        }
        params.set('page', page);

        fetch(`${apiUrl}?${params.toString()}`)
            .then(response => {
                if (!response.ok) throw new Error('Erro na requisição');
                return response.json();
            })
            .then(data => renderResults(data))
            .catch(err => {
                console.error("Erro:", err);
                resultsDiv.innerHTML = `
                    <div class="alert alert-danger text-center">
                        Erro ao carregar dados. Por favor, tente novamente.
                    </div>`;
            })
            .finally(() => {
                // Libera a trava e reabilita o botão original
                isSearching = false;
                submitBtn.disabled = false;
                resultsDiv.style.opacity = '1';
            });
    }

    function renderResults(data) {
        if (!data.results || data.results.length === 0) {
            resultsDiv.innerHTML = '<h3 class="fs-4 fw-semibold text-dark mb-3">Nenhum resultado encontrado</h3>';
            return;
        }

        const detailUrlTemplate = form.dataset.detailUrl;

        const itemsHtml = data.results.map(item => {
            const finalDetailUrl = detailUrlTemplate.replace('__slug__', item.slug);

            return `
            <li class="list-group-item bg-white p-3 rounded shadow-sm mb-2">
                <a class="fw-semibold text-primary-blue mb-1" href="${finalDetailUrl}">
                    Defeito: ${item.defeito_descricao}
                </a>
                <p class="small text-muted mb-0">Modelo: ${item.modelo_descricao} | Marca: ${item.marca_descricao}</p>
            </li>
        `;
        }).join('');

        const paginationHtml = data.page_range.map(p => {
            if (p === '...') return `<li class="page-item disabled"><span class="page-link border-0">...</span></li>`;
            const activeClass = p === data.current_page ? 'active' : '';
            return `<li class="page-item ${activeClass}"><a href="#" class="page-link pagination-link" data-page="${p}">${p}</a></li>`;
        }).join('');

        resultsDiv.innerHTML = `
            <h3 class="fs-4 fw-semibold text-dark mb-3">Resultados Encontrados (${data.count})</h3>
            <ul class="list-unstyled space-y-3">${itemsHtml}</ul>
            <nav aria-label="Navegação de Resultados">
                <ul class="pagination justify-content-center mt-4">
                    <li class="page-item ${!data.has_prev ? 'disabled' : ''}">
                        <a href="#" class="page-link pagination-link" data-page="${data.current_page - 1}">«</a>
                    </li>
                    ${paginationHtml}
                    <li class="page-item ${!data.has_next ? 'disabled' : ''}">
                        <a href="#" class="page-link pagination-link" data-page="${data.current_page + 1}">»</a>
                    </li>
                </ul>
            </nav>
        `;
    }

    // Eventos
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        repair_search(1);
    });

    resultsDiv.addEventListener('click', function (event) {
        const link = event.target.closest('.pagination-link');
        if (!link || isSearching) return;
        event.preventDefault();

        repair_search(link.dataset.page);
        window.scrollTo({top: form.offsetTop - 100, behavior: 'smooth'});
    });
    // Carga inicial
    repair_search(1);
});