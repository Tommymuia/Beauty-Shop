import React from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import AdminLayout from '../layouts/AdminLayout';
import Home from '../pages/Home';
import ProductDetails from '../features/products/ProductDetails';
import Cart from '../features/cart/Cart';
import Checkout from '../features/orders/Checkout';
import Invoice from '../features/orders/Invoice';
import CategoryPage from '../pages/CategoryPage';
import Login from '../features/auth/Login';
import Register from '../features/auth/Register';
import ProfileRouter from '../features/auth/ProfileRouter';
import Wishlist from '../features/wishlist/Wishlist';
import ContactUs from '../pages/ContactUs';
import OrderTracking from '../pages/OrderTracking';
import NewArrivals from '../pages/NewArrivals';
import About from '../pages/About';
import AdminDashboard from '../features/admin/Dashboard';
import ManageProducts from '../features/admin/ManageProducts';
import ManageOrders from '../features/admin/ManageOrders';
import ManageUsers from '../features/admin/ManageUsers';
import AnalyticsReports from '../features/admin/AnalyticsReports';
import Roles from '../features/admin/Roles';
import AddProduct from '../features/admin/AddProduct';
import EditProduct from '../features/admin/EditProduct';
import OrderDetails from '../features/admin/OrderDetails';
import AdminProfile from '../features/admin/AdminProfile';
import CustomerSupport from '../features/admin/CustomerSupport';
import AddUser from '../features/admin/AddUser';
import AdminProductView from '../features/admin/AdminProductView';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout><Home /></MainLayout>} />
      
      {/* Auth Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<MainLayout><ProfileRouter /></MainLayout>} />
      
      {/* Feature Pages */}
      <Route path="/wishlist" element={<MainLayout><Wishlist /></MainLayout>} />
      <Route path="/contact" element={<MainLayout><ContactUs /></MainLayout>} />
      <Route path="/order-tracking" element={<MainLayout><OrderTracking /></MainLayout>} />
      <Route path="/new-arrivals" element={<MainLayout><NewArrivals /></MainLayout>} />
      <Route path="/about" element={<MainLayout><About /></MainLayout>} />
      
      {/* Admin Routes */}
      <Route path="/admin" element={<AdminLayout><AdminDashboard /></AdminLayout>} />
      <Route path="/admin/profile" element={<AdminLayout><AdminProfile /></AdminLayout>} />
      <Route path="/admin/products" element={<AdminLayout><ManageProducts /></AdminLayout>} />
      <Route path="/admin/products/new" element={<AdminLayout><AddProduct /></AdminLayout>} />
      <Route path="/admin/products/view/:id" element={<AdminLayout><AdminProductView /></AdminLayout>} />
      <Route path="/admin/products/edit/:id" element={<AdminLayout><EditProduct /></AdminLayout>} />
      <Route path="/admin/orders" element={<AdminLayout><ManageOrders /></AdminLayout>} />
      <Route path="/admin/orders/:id" element={<AdminLayout><OrderDetails /></AdminLayout>} />
      <Route path="/admin/users" element={<AdminLayout><ManageUsers /></AdminLayout>} />
      <Route path="/admin/users/new" element={<AdminLayout><AddUser /></AdminLayout>} />
      <Route path="/admin/support" element={<AdminLayout><CustomerSupport /></AdminLayout>} />
      <Route path="/admin/analytics" element={<AdminLayout><AnalyticsReports /></AdminLayout>} />
      <Route path="/admin/reports" element={<AdminLayout><AnalyticsReports /></AdminLayout>} />
      <Route path="/admin/roles" element={<AdminLayout><Roles /></AdminLayout>} />
      
      {/* Dynamic Category Route */}
      <Route path="/:category" element={<MainLayout><CategoryPage /></MainLayout>} />
      
      <Route path="/product/:id" element={<MainLayout><ProductDetails /></MainLayout>} />
      <Route path="/cart" element={<MainLayout><Cart /></MainLayout>} />
      <Route path="/checkout" element={<MainLayout><Checkout /></MainLayout>} />
      <Route path="/invoice/:orderId" element={<MainLayout><Invoice /></MainLayout>} />
    </Routes>
  );
};

export default AppRoutes;