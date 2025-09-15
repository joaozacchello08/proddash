import { useState } from "react"
import { Link } from "react-router-dom"
import "./Product.css"
import blankAsset from "../../assets/blank-asset.png"

export default function Product({ id, productName, productImage, productPrice, productStock, preview=false }) {
    const [showConfirm, setShowConfirm] = useState(false)
    const [action, setAction] = useState(null)
    const [bgColor, setBgColor] = useState("")
 
    productPrice = productPrice.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })

    const handleConfirm = () => {
        if (action === "delete") {
            console.log("Deletar produto id:", id)

        } else if (action === "sell") {
            console.log("Vender produto id:", id)

        }
        setShowConfirm(false)
        setAction(null)
    }

    return (
        <>
            <div className="product-card">
                <div className="edit-icon">{preview ? "✏️" : <Link to={`/editar-produto/${id}`}>✏️</Link>}</div>
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
                        <button onClick={handleConfirm} style={{ backgroundColor: bgColor }}>Confirmar</button>
                        <button onClick={() => setShowConfirm(false)}>Cancelar</button>
                    </div>
                </div>
            )}
        </>
    )
}
