import { useEffect, useState } from "react"
import "./HandleProduto.css"
import { useNavigate, useParams } from "react-router-dom"
import { useCookies } from "react-cookie"
import Header from "../../components/header/Header"

function EditarProduto() {
    let params = useParams()
    const id = params.id
    const [cookie] = useCookies(["accessToken"])
    const accessToken = cookie["accessToken"]
    const navigate = useNavigate()
    const [productData, setProductData] = useState([])



    if (!accessToken) return (
        <p>Você não está autenticado.</p>
    )

    if (!id) return (
        <p>Não foi possivel identificar o produto.</p>
    )

    useEffect(() => {
        try {
            const fetchProduct = async () => {
                const response = await fetch(`http://localhost:6969/api/products/${id}/`, { method: "GET", headers: { Authorization: `Bearer ${accessToken}` } })

                if (!response.ok) {
                    alert("Não foi possível encontrar o produto.")
                    navigate("/")
                }
                
                const data = await response.json()
                const product = data.product
                if (!product) {
                    alert("Produto não encontrado")
                    navigate("/")
                }
                setProductData(product)
            }

            fetchProduct()
        } catch(err) {
            alert(`Error: ${err}`)
            navigate("/")
        }
    }, [accessToken, id])

    return (
        <div>
            <Header />

            <div className="product-container">
                <form className="product-form">
                    <h2>Editar Produto</h2>
                    <div className="form-group">
                        <label>Nome do Produto</label>
                        <input type="text" maxLength={100} value={productData.productName} />
                    </div>
                    <div className="form-group">
                        <label>Imagem</label>
                        <input
                            type="file"
                            accept="image/*"
                            
                        />
                    </div>
                </form>
            </div>
        </div>
    )
}

export { EditarProduto }
