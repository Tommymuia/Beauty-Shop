import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ordersAPI } from '../../services/api';
import { CheckCircle, Package, Truck, MapPin, Mail, Phone, Printer, ArrowRight } from 'lucide-react';

const OrderConfirmation = () => {
  const { orderId } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await ordersAPI.getById(orderId);
        const orderData = response.data;
        
        // Handle both formats
        if (orderData.customer) {
          orderData.customer = orderData.customer;
        } else if (typeof orderData.customer_json === 'string') {
          orderData.customer = JSON.parse(orderData.customer_json);
        } else if (orderData.customer_json) {
          orderData.customer = orderData.customer_json;
        }
        
        if (orderData.items) {
          orderData.items = orderData.items;
        } else if (typeof orderData.items_json === 'string') {
          orderData.items = JSON.parse(orderData.items_json);
        } else if (orderData.items_json) {
          orderData.items = orderData.items_json;
        }
        
        orderData.total = orderData.total || orderData.total_amount;
        orderData.createdAt = orderData.createdAt || orderData.created_at;
        
        setOrder(orderData);
      } catch (error) {
        console.error('Error fetching order:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchOrder();
  }, [orderId]);

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600"></div>
      </div>
    );
  }

  if (!order || !order.customer) {
    return (
      <div className="p-20 text-center">
        <h2 className="text-xl font-bold text-gray-800">Order Not Found</h2>
        <button onClick={() => navigate('/')} className="mt-4 text-pink-600 underline">Return Home</button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      {/* Success Header */}
      <div className="text-center mb-10">
        <div className="flex justify-center mb-4">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center">
            <CheckCircle size={48} className="text-green-600" />
          </div>
        </div>
        <h1 className="text-3xl font-serif text-gray-900 mb-2">Order Confirmed!</h1>
        <p className="text-lg text-gray-700 mb-1">Thank you for your purchase, {order.customer.firstName}!</p>
        <p className="text-gray-500">Order #{order.id}</p>
      </div>

      {/* Order Status Timeline */}
      <div className="bg-gradient-to-r from-pink-50 to-purple-50 rounded-2xl p-6 mb-8">
        <div className="flex justify-between items-center">
          <div className="flex flex-col items-center flex-1">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mb-2">
              <CheckCircle size={24} className="text-white" />
            </div>
            <p className="text-sm font-medium text-gray-900">Order Placed</p>
            <p className="text-xs text-gray-500">{new Date(order.createdAt).toLocaleDateString()}</p>
          </div>
          <div className="flex-1 h-1 bg-gray-300 mx-2"></div>
          <div className="flex flex-col items-center flex-1">
            <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mb-2">
              <Package size={24} className="text-white" />
            </div>
            <p className="text-sm font-medium text-gray-500">Processing</p>
            <p className="text-xs text-gray-400">1-2 days</p>
          </div>
          <div className="flex-1 h-1 bg-gray-300 mx-2"></div>
          <div className="flex flex-col items-center flex-1">
            <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center mb-2">
              <Truck size={24} className="text-white" />
            </div>
            <p className="text-sm font-medium text-gray-500">Shipped</p>
            <p className="text-xs text-gray-400">3-5 days</p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Delivery Details */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center gap-2 mb-4">
            <MapPin size={20} className="text-pink-600" />
            <h3 className="text-lg font-serif text-gray-900">Delivery Address</h3>
          </div>
          <div className="space-y-2 text-gray-700">
            <p className="font-medium">{order.customer.firstName} {order.customer.lastName}</p>
            <p>{order.customer.address}</p>
            <p>{order.customer.city}, {order.customer.zip}</p>
          </div>
        </div>

        {/* Contact Details */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <div className="flex items-center gap-2 mb-4">
            <Mail size={20} className="text-pink-600" />
            <h3 className="text-lg font-serif text-gray-900">Contact Information</h3>
          </div>
          <div className="space-y-2 text-gray-700">
            <div className="flex items-center gap-2">
              <Mail size={16} className="text-gray-400" />
              <p>{order.customer.email}</p>
            </div>
            <p className="text-sm text-gray-500">A confirmation email has been sent to this address</p>
          </div>
        </div>
      </div>

      {/* Order Items */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
        <h3 className="text-lg font-serif text-gray-900 mb-4">Order Items</h3>
        <div className="space-y-4">
          {order.items.map((item, idx) => (
            <div key={idx} className="flex justify-between items-center py-3 border-b border-gray-100 last:border-0">
              <div className="flex-1">
                <p className="font-medium text-gray-900">{item.name}</p>
                <p className="text-sm text-gray-500">Quantity: {item.quantity}</p>
              </div>
              <p className="font-medium text-gray-900">Kshs. {(item.totalPrice || item.price * item.quantity).toLocaleString()}</p>
            </div>
          ))}
        </div>
        <div className="border-t border-gray-200 mt-4 pt-4 flex justify-between items-center">
          <span className="text-lg font-bold text-gray-900">Total</span>
          <span className="text-2xl font-bold text-pink-600">Kshs. {order.total.toLocaleString()}</span>
        </div>
      </div>

      {/* Payment Status */}
      <div className="bg-green-50 rounded-2xl border border-green-200 p-6 mb-8">
        <div className="flex items-center gap-3">
          <CheckCircle size={24} className="text-green-600" />
          <div>
            <p className="font-medium text-green-900">Payment Confirmed</p>
            <p className="text-sm text-green-700">Your payment has been successfully processed</p>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          onClick={() => navigate('/orders')}
          className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-900 text-white rounded-full font-medium hover:bg-gray-800 transition-colors"
        >
          View Order History
          <ArrowRight size={18} />
        </button>
        <button
          onClick={() => navigate(`/invoice/${order.id}`)}
          className="flex items-center justify-center gap-2 px-6 py-3 border-2 border-gray-900 text-gray-900 rounded-full font-medium hover:bg-gray-50 transition-colors"
        >
          <Printer size={18} />
          View Invoice
        </button>
        <button
          onClick={() => navigate('/')}
          className="flex items-center justify-center gap-2 px-6 py-3 border border-gray-300 text-gray-700 rounded-full font-medium hover:bg-gray-50 transition-colors"
        >
          Continue Shopping
        </button>
      </div>

      {/* Help Section */}
      <div className="mt-12 text-center">
        <p className="text-gray-600 mb-2">Need help with your order?</p>
        <button
          onClick={() => navigate('/contact')}
          className="text-pink-600 font-medium hover:text-pink-700"
        >
          Contact Support
        </button>
      </div>
    </div>
  );
};

export default OrderConfirmation;
