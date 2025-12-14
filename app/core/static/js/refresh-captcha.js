/* global: fetch, document */
/* Script para recarregar a imagem do CAPTCHA via AJAX. */

(function () {

    const refreshButton = document.querySelector('.captcha-refresh');
    const refreshUrl = '/captcha/refresh/';

    if (!refreshButton) {
        console.warn('Elemento com a classe ".captcha-refresh" não encontrado.');
        return;
    }

    function findCaptchaElements() {
        // ID gerado para o wrapper do campo 'captcha'
        const captchaWrapper = document.getElementById('div_id_captcha');

        if (!captchaWrapper) {
            console.error('DIV wrapper com ID "div_id_captcha" não encontrada.');
            return { hiddenInput: null, img: null };
        }

        // 1. Encontra o input escondido (key/hash)
        const hiddenInput = captchaWrapper.querySelector('input[name="captcha_0"]');

        // 2. Encontra a tag img.
        //    Procura a única imagem dentro desse wrapper que não seja o botão (se houver outro).
        //    A tag img do captcha é geralmente a única tag <img> dentro deste wrapper.
        const img = captchaWrapper.querySelector('img');

        return { hiddenInput, img };
    }

    function handleRefresh(event) {
        event.preventDefault();

        const { hiddenInput, img } = findCaptchaElements();

        if (!hiddenInput || !img) {
            console.error('Campos do CAPTCHA (input ou imagem) não encontrados no DOM.');
            return;
        }

        // Desabilita o botão para evitar cliques múltiplos
        refreshButton.disabled = true;
        refreshButton.classList.add('disabled');

        fetch(refreshUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro de rede: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.key && data.image_url) {
                hiddenInput.value = data.key;
                img.setAttribute('src', data.image_url);
            } else {
                throw new Error('Resposta JSON do servidor inválida.');
            }
        })
        .catch(error => {
            console.error('Erro ao recarregar o CAPTCHA:', error);
            alert('Houve um erro ao carregar o novo CAPTCHA.');
        })
        .finally(() => {
            // Reabilita o botão após a conclusão
            refreshButton.disabled = false;
            refreshButton.classList.remove('disabled');
        });
    }

    refreshButton.addEventListener('click', handleRefresh);

})();