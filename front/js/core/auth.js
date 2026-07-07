/*
|--------------------------------------------------------------------------
| LOGIN
|--------------------------------------------------------------------------
*/

document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("formLogin");

    if (!form) return;

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;
        const erro  = document.getElementById("erroLogin");

        erro.innerHTML = "";

        try {

            const response = await api.post("/api/user/login", {
                email:    email,
                password: senha,
            });

            /*
            |--------------------------------------------------------------------------
            | SALVAR TOKEN E REDIRECIONAR
            |--------------------------------------------------------------------------
            */

            const token = response.data.resultado.access_token;

            localStorage.setItem("token", token);

            window.location.href = "/index";

        } catch (err) {

            console.error(err);

            if (err.response?.status === 401) {
                erro.innerHTML = "E-mail ou senha inválidos";
                return;
            }

            erro.innerHTML = "Erro ao conectar com a API";

        }

    });

});