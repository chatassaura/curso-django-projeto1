function my_scope() {
    // 1. Selecionamos TODOS os formulários de exclusão
    const forms = document.querySelectorAll('.form-delete');

    // 2. Percorremos cada formulário encontrado
    forms.forEach(form => {
        // 3. Adicionamos o "ouvinte" de eventos em cada um deles individualmente
        form.addEventListener('submit', function (e) {
            e.preventDefault(); // Impede o envio imediato do formulário clicado

            const confirmed = confirm('Deseja realmente excluir esta receita?');

            if (confirmed) {
                // 4. Se confirmado, envia apenas ESTE formulário específico
                form.submit();
            }
        });
    });
}

my_scope();