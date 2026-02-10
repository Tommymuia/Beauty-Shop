import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ordersAPI } from '../../services/api';
import { CheckCircle, Printer, Loader2 } from 'lucide-react';

const Invoice = () => {
  const { orderId } = useParams(); // Get ID from URL
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await ordersAPI.getById(orderId);
        const orderData = response.data;
        
        // Handle both formats: direct objects or JSON strings
        if (orderData.customer) {
          // Already an object from OrderDetailResponse
          orderData.customer = orderData.customer;
        } else if (typeof orderData.customer_json === 'string') {
          orderData.customer = JSON.parse(orderData.customer_json);
        } else if (orderData.customer_json) {
          orderData.customer = orderData.customer_json;
        }
        
        if (orderData.items) {
          // Already an array from OrderDetailResponse
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

  if (loading) return <div className="flex h-screen items-center justify-center"><Loader2 className="animate-spin" /></div>;

  if (!order || !order.customer) {
    return (
      <div className="p-20 text-center">
        <h2 className="text-xl font-bold text-gray-800">Order Not Found</h2>
        <p className="text-gray-500 mb-4">We couldn't find an invoice with ID: {orderId}</p>
        <button onClick={() => navigate('/')} className="text-pink-600 underline">Return Home</button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <div className="text-center mb-10">
        <div className="flex justify-center mb-4 text-green-500"><CheckCircle size={64} /></div>
        <h1 className="text-3xl font-serif text-gray-900 mb-2">Thank You for Shopping with Us!</h1>
        <p className="text-lg text-gray-700 mb-2">Your order has been successfully placed</p>
        <p className="text-gray-500">A confirmation email has been sent to {order.customer?.email || 'your email'}</p>
      </div>

      <div className="bg-white border border-gray-200 p-8 rounded-xl shadow-sm print:shadow-none print:border-none">
        <div className="flex justify-between items-center border-b border-gray-100 pb-6 mb-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900">INVOICE</h2>
            <p className="text-sm text-gray-500">#{order.id}</p>
          </div>
          <div className="text-right">
            <p className="font-bold text-gray-900">Bloom Beauty</p>
            <p className="text-sm text-gray-500">{new Date(order.createdAt).toLocaleDateString()}</p>
          </div>
        </div>

        <div className="mb-8 grid grid-cols-2">
          <div>
            <h3 className="text-xs font-bold uppercase text-gray-400 mb-2">Bill To:</h3>
            <p className="font-bold text-gray-900">{order.customer.firstName} {order.customer.lastName}</p>
            <p className="text-gray-600">{order.customer.address}</p>
            <p className="text-gray-600">{order.customer.city}, {order.customer.zip}</p>
          </div>
          <div className="text-right">
             <h3 className="text-xs font-bold uppercase text-gray-400 mb-2">Status:</h3>
             <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-bold">{order.status || 'Paid'}</span>
          </div>
        </div>

        <table className="w-full mb-8">
          <thead>
            <tr className="text-left text-xs uppercase text-gray-400 border-b border-gray-100">
              <th className="pb-3">Item</th>
              <th className="pb-3 text-center">Qty</th>
              <th className="pb-3 text-right">Price</th>
            </tr>
          </thead>
          <tbody className="text-sm text-gray-700">
            {order.items.map((item, idx) => (
              <tr key={idx} className="border-b border-gray-50">
                <td className="py-3">{item.name}</td>
                <td className="py-3 text-center">{item.quantity}</td>
                <td className="py-3 text-right">Kshs. {(item.totalPrice || item.price * item.quantity).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="flex justify-between items-center pt-4">
          <span className="font-bold text-lg">Total Paid</span>
          <span className="font-bold text-2xl text-pink-600">Kshs. {order.total.toLocaleString()}</span>
        </div>
      </div>

      <div className="flex justify-center space-x-4 mt-8 print:hidden">
        <button onClick={() => window.print()} className="flex items-center gap-2 text-gray-600 hover:text-gray-900">
          <Printer size={18} /> Print Invoice
        </button>
        <button onClick={() => navigate('/')} className="bg-gray-900 text-white px-6 py-2 rounded-full hover:bg-gray-800">
          Continue Shopping
        </button>
      </div>
    </div>
  );
};

export default Invoice;