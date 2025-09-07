import Header from "../../components/header/Header"
import Product from "../../components/product/Product"
import { useState } from "react"
import blankAsset from "../../assets/blank-asset.png"
import "./AddProduto.css"
import { useCookies } from "react-cookie"

export default function AddProdutoPage() {
    const [name, setName] = useState("")
    const [cost, setCost] = useState(0)
    const [price, setPrice] = useState(0)
    const [image, setImage] = useState("")
    const [stock, setStock] = useState(0)
    const [barcode, setBarcode] = useState("")

    let [cookies] = useCookies(["accessToken"])
    let accessToken = cookies["accessToken"]

    const handleImageUpload = (e) => {
        const file = e.target.files[0]
        if (!file) return

        const reader = new FileReader()

        reader.onloadend = () => {
            setImage(reader.result)
        }

        reader.readAsDataURL(file)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (!accessToken) alert("Não foi possível concluir a operação, pois não foi encontrado o token de acesso (nenhuma conta está logada).")
        else {
            const response = await fetch("http://localhost:6969/api/products/", {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                    "X-API-KEY": import.meta.env.VITE_SECRET_KEY,
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    productName: name,
                    productPrice: price,
                    productCost: cost,
                    productImage: image,
                    productBarcode: barcode,
                    productStock: stock
                }),
            })

            const data = await response.json()

            if (!response.ok) alert(`An error occurred: ${response.message}`)
            else alert("Produto adicionado com sucesso!")

            // console.log(JSON.stringify(data, null, 2))
        }
    }

    return (
        <div>
            <Header />

            <div className="add-product-container">
                <form className="add-product-form" onSubmit={handleSubmit}>
                    <h2>Adicionar Novo Produto</h2>
                    <div className="form-group">
                        <label>Nome do Produto <span className="required-input-warn" title="Campo obrigatório">*</span></label>
                        <input type="text" onChange={(e) => setName(e.target.value)} maxLength={100} required />
                    </div>
                    <div className="form-group">
                        <label>Imagem</label>
                        <input type="file" accept="image/*" onChange={handleImageUpload} />
                    </div>
                    <div className="form-group">
                        <label>Preço <span className="required-input-warn" title="Campo obrigatório">*</span></label>
                        <input type="number" onChange={(e) => setPrice(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>Custo <span className="required-input-warn" title="Campo obrigatório">*</span></label>
                        <input type="number" onChange={(e) => setCost(e.target.value)} required />
                    </div>
                    <div className="form-group">
                        <label>Estoque</label>
                        <input type="number" onChange={(e) => setStock(e.target.value)} />
                    </div>
                    <div className="form-group">
                        <label>Código de Barras</label>
                        <input type="text" maxLength={14} onChange={(e) => setBarcode(e.target.value)} />
                    </div>

                    <button type="submit" className="submit-button">ADICIONAR</button>
                </form>

                <div className="preview-container">
                    {name && price ? (
                        <Product
                            id={"Preview"}
                            productName={name}
                            productImage={image || blankAsset}
                            productPrice={price}
                            productStock={stock}
                        />
                    ) : (
                        <h2>PREVIEW DO CARD AQUI</h2>
                    )}
                </div>
            </div>
        </div>
    )
}
