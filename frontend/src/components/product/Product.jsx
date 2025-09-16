import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import "./Product.css"
import blankAsset from "../../assets/blank-asset.png"
import { useCookies } from "react-cookie"

export default function Product({ id, productName, productImage, productPrice, productStock, preview=false }) {
    const [cookie] = useCookies(["accessToken"])
    const [showConfirm, setShowConfirm] = useState(false)
    const [action, setAction] = useState(null)
    const [bgColor, setBgColor] = useState("")
    const navigate = useNavigate()
    const [description, setDescription] = useState("")
    const [amount, setAmount] = useState(1)

 
    productPrice = productPrice.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })

    const handleConfirm = async (e) => {
        e.preventDefault()

        const accessToken = cookie["accessToken"]
        if (!accessToken) {
            alert("Você não está autenticado.")
            setShowConfirm(false)
            setAction(null)
        } else {
            if (action === "delete") {
                const response = await fetch(`http://localhost:6969/api/products/${id}`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${accessToken}` }
                })

                const data = await response.json()

                if (!response.ok) {
                    alert("Não foi possível deletar o produto.")
                    console.log(data)
                } else {
                    alert("Produto deletado com sucesso!")
                    navigate(0)
                }
            } else if (action === "sell") {
                const response = await fetch(`http://localhost:6969/api/sales/${id}`, {
                    method: "POST",
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                        "Content-type": "application/json"
                    },
                    body: JSON.stringify({ description: description, soldAmount: amount })
                })

                const data = await response.json()
                if (!response.ok) {
                    alert("Não foi possível realizar a venda do produto.")
                    console.log(data)
                } else {
                    alert("Venda registrada com sucesso!")
                    navigate(0)
                }
            }
        }

        setShowConfirm(false)
        setAction(null)
    }

    return (
        <>
            <div className="product-card">
                <div className="edit-icon">{preview ? "✏️" : <Link style={{ textDecoration: "none" }} to={`/editar-produto/${id}`}>✏️</Link>}</div>
                <div className="confirm-icon" onClick={() => { if (!preview) setShowConfirm(true); setAction("sell"); setBgColor("#27ae60") }}>✅</div>
                <div className="delete-icon" onClick={() => { if (!preview) setShowConfirm(true); setAction("delete"); setBgColor("#e74c3c") }}>❌</div>
                <div className="product-details">
                    <h3>{productName}</h3>
                    <img src={productImage || blankAsset} alt={productName} />
                    <p>R$ {productPrice}</p>
                    <p>ESTOQUE: {productStock}</p>
                    <p>Id: {id}</p>
                </div>
            </div>

            {showConfirm && (
                <div className="modal-overlay">
                    <div className="modal" tabIndex={-1} autoFocus>
                    <p>
                        Tem certeza que deseja {action === "delete" ? "deletar" : "vender"} este produto?
                    </p>

                    {action === "sell" && (
                        <form onSubmit={handleConfirm} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                        <input
                            type="text"
                            placeholder="Descrição (opcional)"
                            value={description}
                            maxLength={250}
                            onChange={e => setDescription(e.target.value)}
                        />
                        <input
                            type="number"
                            placeholder="Quantidade (opcional)"
                            value={amount}
                            onChange={e => setAmount(e.target.value)}
                            min="1"
                            max={productStock}
                        />
                        <button type="submit" style={{ backgroundColor: bgColor }}>Confirmar</button>
                        </form>
                    )}

                    {action === "delete" && (
                        <>
                        <button onClick={handleConfirm} style={{ backgroundColor: bgColor }}>Confirmar</button>
                        </>
                    )}

                    <button onClick={() => setShowConfirm(false)}>Cancelar</button>
                    </div>
                </div>
            )}
        </>
    )
}
