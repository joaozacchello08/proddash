import "./Product.css"

export default function Product({ id, productName, productImage, productPrice, productStock }) {
    return (
        <div className="product-card">
            <div className="edit-icon">✏️</div>
            <div className="confirm-icon">✅</div>
            <div className="delete-icon">❌</div>
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