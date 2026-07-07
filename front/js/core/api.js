const API = "http://localhost:3001";

/*
|--------------------------------------------------------------------------
| INSTÂNCIA AXIOS
|--------------------------------------------------------------------------
*/

const axiosInstance = axios.create({

    baseURL: API,

    headers: {
        "Content-Type": "application/json"
    }

});

/*
|--------------------------------------------------------------------------
| TOKEN AUTOMÁTICO
|--------------------------------------------------------------------------
*/

axiosInstance.interceptors.request.use((config) => {

    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;

});

/*
|--------------------------------------------------------------------------
| RESPONSE INTERCEPTOR
|--------------------------------------------------------------------------
*/

axiosInstance.interceptors.response.use(

    (response) => response,

    (error) => {

        if (
            error.response?.status === 401 ||
            error.response?.status === 403
        ) {
            logout();
        }

        return Promise.reject(error);

    }

);

/*
|--------------------------------------------------------------------------
| API — MÉTODOS PRONTOS
|--------------------------------------------------------------------------
*/

const api = {
    get: (url) => axiosInstance.get(url).then(r => r.data),

    post: (url, body, config = {}) =>
        axiosInstance.post(url, body, config).then(r => r.data),

    put: (url, body) =>
        axiosInstance.put(url, body).then(r => r.data),

    delete: (url) =>
        axiosInstance.delete(url).then(r => r.data),
    getBlob: (url) =>
        axiosInstance.get(url, {
            responseType: 'blob'
        }).then(r => r.data)
};

/*
|--------------------------------------------------------------------------
| VERIFICAR LOGIN
|--------------------------------------------------------------------------
*/

function verificarLogin() {

    if (!localStorage.getItem("token")) {
        window.location.href = "/login";
    }

}

/*
|--------------------------------------------------------------------------
| LOGOUT
|--------------------------------------------------------------------------
*/

function logout() {

    localStorage.removeItem("token");

    window.location.href = "/login";

}