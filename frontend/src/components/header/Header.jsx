import { Link } from "react-router-dom"
import "./Header.css"

export default function Header() {
    return (
        <header className="header">
            <div className="logo"><Link to={"/"} className="nav-link">ProdDash</Link></div>
            <nav className="nav-links">
                <Link to={"/"} className="nav-link">Dashboard</Link>
                <Link to={"/novo-produto"} className="nav-link">Adicionar produto</Link>
                <Link to={"#"} className="nav-link">Vendas</Link>
                <Link to={"#"} className="nav-link">Lucro</Link>
                <Link to={"/usuario"} className="nav-link">Usuário</Link>
            </nav>
        </header>
    )
}
