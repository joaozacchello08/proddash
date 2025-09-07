import "./AddUser.css"
import { useEffect, useState } from "react"
import Header from "../../components/header/Header"
import { useNavigate } from "react-router-dom"
import { useCookies } from "react-cookie"

function AddUser() {
    const [mode, setMode] = useState("register") // "register" ou "login"
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [identifier, setIdentifier] = useState("") // email ou username para login
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [cookies, setCookie] = useCookies(["accessToken"])
    const navigate = useNavigate()

    const validateRegister = () => {
        if (!email.trim() || !username.trim()) {
            alert("Informe um email e um nome de usuário.")
            return false
        }
        if (!password) {
            alert("Informe uma senha.")
            return false
        }
        if (password.length > 64) {
            alert("A senha deve ter no máximo 64 caracteres.")
            return false
        }
        return true
    }

    const validateLogin = () => {
        if (!identifier.trim()) {
            alert("Informe seu email ou nome de usuário.")
            return false
        }
        if (!password) {
            alert("Informe sua senha.")
            return false
        }
        return true
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (mode === "register" && !validateRegister()) return
        if (mode === "login" && !validateLogin()) return

        setLoading(true)
        try {
            const url =
                mode === "register"
                    ? "http://localhost:6969/api/users/"
                    : "http://localhost:6969/api/users/login"

            const body =
                mode === "register"
                    ? { email, username, password }
                    : { identifier, password }

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "X-API-KEY": import.meta.env.VITE_SECRET_KEY,
                },
                body: JSON.stringify(body),
            })

            const data = await response.json()
            if (!response.ok) {
                alert(`Erro: ${data.message || "Algo deu errado"}`)
            } else {
                const accessToken = data.accessToken
                setCookie("accessToken", accessToken, {
                    path: "/",
                    maxAge: 60 * 60 * 24 * 365 * 10, // 10 anos
                    sameSite: "strict",
                })
                alert(mode === "register" ? "Usuário criado com sucesso!" : "Login realizado com sucesso!")
                navigate("/")
            }
        } catch (err) {
            alert(`Algum erro estranho aconteceu. Erro: ${err}`)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <Header />

            <div className="add-user-container">
                <form className="add-user-form" onSubmit={handleSubmit}>
                    <h2>{mode === "register" ? "Registrar Usuário" : "Login"}</h2>

                    <div className="mode-switch">
                        <button
                            type="button"
                            className={mode === "register" ? "active" : ""}
                            onClick={() => setMode("register")}
                        >
                            Registrar
                        </button>
                        <button
                            type="button"
                            className={mode === "login" ? "active" : ""}
                            onClick={() => setMode("login")}
                        >
                            Login
                        </button>
                    </div>

                    {mode === "register" && (
                        <>
                            <div className="form-group">
                                <label>Email <span className="required-input-warn">*</span></label>
                                <input
                                    type="email"
                                    onChange={(e) => setEmail(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Nome de Usuário <span className="required-input-warn">*</span></label>
                                <input
                                    type="text"
                                    maxLength={50}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                        </>
                    )}

                    {mode === "login" && (
                        <div className="form-group">
                            <label>Email ou Nome de Usuário <span className="required-input-warn">*</span></label>
                            <input
                                type="text"
                                onChange={(e) => setIdentifier(e.target.value)}
                                required
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>Senha <span className="required-input-warn">*</span></label>
                        <input
                            type="password"
                            maxLength={64}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? (mode === "register" ? "Registrando..." : "Logando...") : (mode === "register" ? "Registrar" : "Login")}
                    </button>
                </form>
            </div>
        </div>
    )
}

function Profile() {
    return <h1>PROFILE</h1>
}

export default function Usuario() {
    const [cookies] = useCookies(["accessToken"])
    const [logged, setLogged] = useState(false)

    useEffect(() => {
        if (!cookies["accessToken"]) setLogged(false)
        else setLogged(true)
    }, [cookies])

    return (
        <>
            {logged ? <Profile /> : <AddUser />}
        </>
    )
}
