import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.jsx'
import AddProdutoPage from './pages/add-produto/AddProduto.jsx'
import { CookiesProvider } from 'react-cookie'
import Usuario from './pages/user/AddUser.jsx'
import { EditarProduto } from './pages/handle-produto/HandleProduto.jsx'
import { Vendas, EditarVenda } from './pages/vendas/Vendas.jsx'
import './index.css'

let router = createBrowserRouter([
  {
    path: "/",
    Component: App,
  },

  {
    path: "/novo-produto",
    Component: AddProdutoPage,
  },
  {
    path: "/editar-produto/:id",
    Component: EditarProduto
  },

  {
    path: "/vendas",
    Component: Vendas
  },
  {
    path: "/vendas/editar-venda/:id",
    Component: EditarVenda
  },

  {
    path: "/usuario",
    Component: Usuario,
  },
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CookiesProvider>
      <RouterProvider router={router} />
    </CookiesProvider>,
  </StrictMode>
)
