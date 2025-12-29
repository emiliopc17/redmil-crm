import { AuthBindings } from "@refinedev/core";

const API_URL = "http://localhost:8000/api/v1";

export const authProvider: AuthBindings = {
    login: async ({ email, password }) => {
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.access_token) {
                localStorage.setItem("token", data.access_token);
                return {
                    success: true,
                    redirectTo: "/",
                };
            } else {
                return {
                    success: false,
                    error: {
                        name: "Login Error",
                        message: data.detail || "Email o contraseña inválidos",
                    },
                };
            }
        } catch (error: any) {
            return {
                success: false,
                error: {
                    name: "Login Error",
                    message: "Error de conexión con el servidor",
                },
            };
        }
    },
    logout: async () => {
        localStorage.removeItem("token");
        return {
            success: true,
            redirectTo: "/login",
        };
    },
    check: async () => {
        const token = localStorage.getItem("token");
        if (token) {
            return {
                authenticated: true,
            };
        }

        return {
            authenticated: false,
            logout: true,
            redirectTo: "/login",
        };
    },
    getPermissions: async () => null,
    getIdentity: async () => {
        const token = localStorage.getItem("token");
        if (token) {
            return {
                id: 1,
                name: "Admin User",
                avatar: "https://i.pravatar.cc/300",
            };
        }
        return null;
    },
    onError: async (error) => {
        if (error.status === 401 || error.status === 403) {
            localStorage.removeItem("token");
            return {
                logout: true,
                redirectTo: "/login",
            };
        }
        return { error };
    },
};
