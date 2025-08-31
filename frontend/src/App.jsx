import Product from "./components/product/Product"
import image from "./assets/image.png"
import { Link } from "react-router-dom"

const products = [
    {
        id: 0,
        productName: "Camiseta Corinthians I 24/25",
        productImage: image,
        productPrice: 249.9,
        productStock: 30
    },
    {
        id: 1,
        productName: "Camiseta Corinthians II 24/25",
        productImage: image,
        productPrice: 229.9,
        productStock: 50
    },
    {
        id: 2,
        productName: "Boné Corinthians Ed. Limitada",
        productImage: image,
        productPrice: 89.9,
        productStock: 15
    },
    {
        id: 3,
        productName: "Jaqueta de Treino Corinthians",
        productImage: image,
        productPrice: 349.9,
        productStock: 25
    },
    {
        id: 4,
        productName: "Cachecol Corinthians",
        productImage: image,
        productPrice: 79.9,
        productStock: 40
    },
    {
        id: 5,
        productName: "Chaveiro Corinthians",
        productImage: image,
        productPrice: 19.9,
        productStock: 100
    },
    {
        id: 6,
        productName: "Copo Térmico Oficial",
        productImage: image,
        productPrice: 119.9,
        productStock: 35
    }
]

export default function App() {
    return (
        <div>
            <header className="header">
                <div className="logo">ProdDash</div>
                <nav className="nav-links">
                    <Link to={"#"} className="nav-link">Dashboard</Link>
                    <Link to={"#"} className="nav-link">Adicionar produto</Link>
                    <Link to={"#"} className="nav-link">Vendas</Link>
                    <Link to={"#"} className="nav-link">Lucro</Link>
                    <Link to={"#"} className="nav-link">Usuário</Link>
                </nav>
            </header>

            <h3 style={{ paddingLeft: 50 }}>A</h3>
            <div className="product-grid">
                {products.map(product => (
                    <Product
                        key={product.id}
                        id={product.id}
                        productName={product.productName}
                        productImage={product.productImage}
                        productPrice={product.productPrice}
                        productStock={product.productStock}
                    />
                ))}
            </div>
        </div>
    )
}
