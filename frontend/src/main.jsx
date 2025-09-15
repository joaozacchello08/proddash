import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import AddProdutoPage from './pages/add-produto/AddProduto.jsx'
import { CookiesProvider } from 'react-cookie'
import Usuario from './pages/user/AddUser.jsx'
import { EditarProduto } from './pages/handle-produto/HandleProduto.jsx'

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
    path: "/usuario",
    Component: Usuario,
  },
])

createRoot(document.getElementById('root')).render(
  <CookiesProvider>
    <RouterProvider router={router} />
  </CookiesProvider>,
)
