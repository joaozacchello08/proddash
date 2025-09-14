import { useEffect, useState } from "react"
import "./HandleProduto.css"
import { useNavigate, useParams } from "react-router-dom"
import { useCookies } from "react-cookie"
import Header from "../../components/header/Header"
import blankAsset from "../../assets/blank-asset.png"
import Product from "../../components/product/Product"

function EditarProduto() {
    let params = useParams()
    const id = params.id
    const [cookie] = useCookies(["accessToken"])
    const accessToken = cookie["accessToken"]
    const navigate = useNavigate()
    const [productData, setProductData] = useState([])

    //edit
    const [name, setName] = useState("")
    const [cost, setCost] = useState(0)
    const [price, setPrice] = useState(0)
    const [image, setImage] = useState("")
    const [stock, setStock] = useState(0)
    const [barcode, setBarcode] = useState("")


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

    const handleImageUpload = (e) => {
        const file = e.target.files[0]
        if (!file) return

        const reader = new FileReader()

        reader.onloadend = () => {
            setImage(reader.result)
        }

        reader.readAsDataURL(file)
    }

    return (
        <div>
            <Header />

            <div className="product-container">
                <form className="product-form">
                    <div style={{ display: "flex", flexDirection: "column" }}>
                        <h2>Editar Produto</h2>
                        <p>Mude os valores do produto para atualizá-los.</p>
                    </div>
                    
                    <div className="form-group">
                        <label>Nome do Produto</label>
                        <input
                            type="text"
                            maxLength={100}
                            value={productData.productName}
                        />
                    </div>
                    <div className="form-group">
                        <label>Imagem</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                        />
                    </div>
                    <div className="form-group">
                        <label>Preço</label>
                        <input
                            type="text"
                            onChange={(e) => setPrice(parseFloat(e.target.value))}
                            value={productData.productPrice}
                        />
                    </div>
                    <div className="form-group">
                        <label>Custo</label>
                        <input
                            type="text"
                            onChange={(e) => setCost(parseFloat(e.target.value))}
                            value={productData.productCost}
                        />
                    </div>
                    <div className="form-group">
                        <label>Estoque</label>
                        <input
                            type="number"
                            onChange={(e) => setStock(e.target.value)}
                            value={productData.productStock}
                        />
                    </div>
                    <div className="form-group">
                        <label>Código de Barras</label>
                        <input
                            type="text"
                            value={productData.productBarcode}
                            onChange={(e) => setBarcode(e.target.value)}
                        />
                    </div>

                    <button type="submit" className="submit-button">ATUALIZAR</button>
                </form>

                <div className="preview-container">
                    {name && price || productData.productName && productData.productPrice ? (
                        <Product
                            id={"Preview"}
                            productName={name || productData.productName}
                            productImage={image || productData.productImage || blankAsset}
                            productPrice={price || productData.productPrice}
                            productStock={stock || productData.productStock}
                        />
                    ) : (
                        <h2>PREVIEW DO CARD AQUI</h2>
                    )}
                </div>
            </div>
        </div>
    )
}

export { EditarProduto }
