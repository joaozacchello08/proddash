import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import AddProdutoPage from './pages/add-produto/AddProduto.jsx'
import { CookiesProvider } from 'react-cookie'

let router = createBrowserRouter([
  {
    path: "/",
    Component: App,
  },
  {
    path: "/novo-produto",
    Component: AddProdutoPage,
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CookiesProvider>
      <RouterProvider router={router} />
    </CookiesProvider>
  </StrictMode>,
)
