class ModalManager {

    static dados = {};

    static iniciar() {

        document.querySelectorAll('.modal').forEach(modal => {

            if (modal.dataset.modalManager == "1")
                return;

            modal.dataset.modalManager = "1";

            modal.addEventListener('show.bs.modal', function () {

                const qtd = document.querySelectorAll('.modal.show').length;

                const zIndex = 1055 + (qtd * 20);

                this.style.zIndex = zIndex;

                setTimeout(() => {

                    const backdrops = document.querySelectorAll('.modal-backdrop');

                    const ultimo = backdrops[backdrops.length - 1];

                    if (ultimo)
                        ultimo.style.zIndex = zIndex - 1;

                });

            });

            modal.addEventListener('hidden.bs.modal', function () {

                if (document.querySelector('.modal.show')) {
                    document.body.classList.add('modal-open');
                }

                delete ModalManager.dados[this.id];

            });

        });

    }

    static abrir(id, dados = {}) {

        ModalManager.dados[id] = dados;

        const modal = bootstrap.Modal.getOrCreateInstance(
            document.getElementById(id)
        );

        modal.show();

    }

    static fechar(id) {

        const modal = bootstrap.Modal.getInstance(
            document.getElementById(id)
        );

        if (modal)
            modal.hide();

    }

    static getDados(id) {

        return ModalManager.dados[id] || {};

    }

}