import "./Product.css"
import { Link } from "react-router-dom"
 
export default function Product({ id, productName, productImage, productPrice, productStock }) {
    productPrice = productPrice.toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    })

    return (
        <div className="product-card">
            <div className="edit-icon"><Link to={`/editar-produto/${id}`}>✏️</Link></div>
            <div className="confirm-icon"><Link to={`/vender-produto/${id}`}>✅</Link></div>
            <div className="delete-icon"><Link to={`/deletar-produto/${id}`}>❌</Link></div>
            <div className="product-details">
                <h3>{productName}</h3>
                <img src={productImage} alt={productName} />
                <p>R$ {productPrice}</p>
                <p>ESTOQUE: {productStock}</p>
                <p>Id: {id}</p>
            </div>
        </div>
    )
}