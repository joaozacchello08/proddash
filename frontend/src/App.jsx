import Product from "./components/product/Product"
import image from "./assets/image.png"
import Header from "./components/header/Header"
import { useNavigate } from "react-router-dom"
import { useCookies } from "react-cookie"
import { useEffect, useState } from "react"

export default function App() {
    const [cookies] = useCookies(["accessToken"])
    const [products, setProducts] = useState([])
    // const [dashboardName, setDashboardName] = useState("")
    const navigate = useNavigate()

    useEffect(() => {
        if (!cookies["accessToken"]) {
            navigate("/usuario")
        } else {
            const fetchProducts = async () => {
                const accessToken = cookies["accessToken"]
                const response = await fetch("http://localhost:6969/api/products/", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${accessToken}` },
                })
                const data = await response.json()
                setProducts(Array.isArray(data) ? data : [])
            }

            fetchProducts()
        }
    }, [cookies, navigate])

    return (
        <div>
            <Header />

            <div className="product-grid">
                {Array.isArray(products) && products.length > 0 ? (
                    products.map(product => (
                        <Product
                            key={product.productId}
                            id={product.productId}
                            productName={product.productName}
                            productImage={product.productImage}
                            productPrice={product.productPrice}
                            productStock={product.productStock}
                        />
                    ))
                ) : (
                    <p>Sem produtos registrados</p>
                )}
            </div>
        </div>
    )
}
