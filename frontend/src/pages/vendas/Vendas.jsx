import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useCookies } from "react-cookie"
import Header from "../../components/header/Header"
import { Link } from "react-router-dom"
import "./Vendas.css"

function Vendas() {
    const [cookie] = useCookies(["accessToken"])
    const accessToken = cookie["accessToken"]
    if (!accessToken) return <p>Você não está autenticado.</p>

    const [sales, setSales] = useState([])
    // const [products, setProducts] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        try {
            const fetchSales = async () => {
                const response = await fetch("http://localhost:6969/api/sales/", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${accessToken}` }
                })

                const data = await response.json() //{ "sales": [sale.serialize() for sale in sales] }

                if (!response.ok) {
                    console.log(data)
                } else {
                    const sales = data.sales // [{}]
                    setSales(sales)
                }
            }

            const fetchProducts = async () => {
                const response = await fetch("http://localhost:6969/api/products/", {
                    method: "GET",
                    headers: { Authorization: `Bearer ${accessToken}` }
                })

                const data = await response.json()

                if (!response.ok) {
                    console.log(data)
                } else {
                    // setProducts(data)
                }
            }

            // fetchProducts()
            fetchSales()
        } catch (err) {
            alert("Um erro ocorreu tentando carregar as vendas.")
            console.log("Erro:", err)
            navigate("/")
        }
    }, [accessToken])

    return (
        <div>
            <Header />

            {/* <h1>{JSON.stringify(sales)}</h1> */}

            <div className="sales-container">
                {sales.length > 0 ? (
                    sales.map(sale => (
                    <div className="sale-card" key={sale.id}>
                        <div className="edit-icon"><Link to={`/vendas/editar-venda/${sale.id}`} style={{ textDecoration: "none" }}>✏️</Link></div>
                        <div className="delete-icon">❌</div>

                        <h3>{sale.product.productName}</h3>
                        <p><strong>Quantidade:</strong> {sale.soldAmount}</p>

                        <p><strong>Preço:</strong> R$ {sale.priceAtSale}</p>
                        <p><strong>Custo:</strong> R$ {sale.costAtSale}</p>

                        <p><strong>Data:</strong> {new Date(sale.soldAt).toLocaleString()}</p>
                        <p><strong>Descrição:</strong> {sale.description || "Sem descrição especificada."}</p>
                    </div>
                    ))
                ) : (
                    <p className="no-sales">Sem vendas registradas.</p>
                )}
            </div>
        </div>
    )
}

function EditarVenda() {
    return <h1>editar vendas</h1>
}

export { Vendas, EditarVenda }
