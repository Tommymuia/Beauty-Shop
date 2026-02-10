import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ordersAPI } from '../../services/api';
import { ArrowLeft, Package, User, MapPin, CreditCard, Calendar, FileText, Truck, Loader2 } from 'lucide-react';

const OrderDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [currentStatus, setCurrentStatus] = useState('');

  useEffect(() => {
    fetchOrderDetails();
  }, [id]);

  const fetchOrderDetails = async () => {
    try {
      const response = await ordersAPI.getById(id);
      const orderData = response.data;
      
      // Parse JSON fields
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
      setCurrentStatus(orderData.status);
    } catch (error) {
      console.error('Failed to fetch order:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateOrderStatus = async (newStatus) => {
    try {
      await ordersAPI.updateStatus(order.id, newStatus);
      setCurrentStatus(newStatus);
      setOrder({ ...order, status: newStatus });
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };

  const generateInvoice = () => {
    navigate(`/admin/orders/${order.id}/invoice`);
  };

  const getStatusColor = (status) => {
    const statusLower = status?.toLowerCase();
    switch (statusLower) {
      case 'processing': return 'bg-yellow-100 text-yellow-800';
      case 'shipped': return 'bg-blue-100 text-blue-800';
      case 'delivered': return 'bg-green-100 text-green-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'paid': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTimelineSteps = () => {
    const statusLower = currentStatus?.toLowerCase();
    return [
      { status: 'Order Placed', completed: true },
      { status: 'Payment Confirmed', completed: statusLower === 'paid' || statusLower === 'processing' || statusLower === 'shipped' || statusLower === 'delivered' },
      { status: 'Processing', completed: statusLower === 'processing' || statusLower === 'shipped' || statusLower === 'delivered' },
      { status: 'Shipped', completed: statusLower === 'shipped' || statusLower === 'delivered' },
      { status: 'Delivered', completed: statusLower === 'delivered' }
    ];
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="animate-spin text-pink-600" size={48} />
      </div>
    );
  }

  if (!order) {
    return (
      <div className="text-center py-12">
        <Package size={64} className="mx-auto text-gray-300 mb-4" />
        <h3 className="text-xl font-medium text-gray-900 mb-2">Order Not Found</h3>
        <button onClick={() => navigate('/admin/orders')} className="text-pink-600 hover:text-pink-700">
          Back to Orders
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4 mb-6">
        <button
          onClick={() => navigate('/admin/orders')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Orders
        </button>
      </div>
      
      <div>
        <h1 className="text-2xl font-serif text-gray-900">Order Details</h1>
        <p className="text-gray-500">Order #{order.id}</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Main Order Info */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Order Items */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-serif text-gray-900 mb-4">Order Items</h2>
            <div className="space-y-4">
              {order.items?.map((item, index) => (
                <div key={index} className="flex items-center gap-4 p-4 border border-gray-100 rounded-xl">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{item.name}</h3>
                    <p className="text-sm text-gray-500">Quantity: {item.quantity}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">Kshs. {(item.totalPrice || item.price * item.quantity)?.toLocaleString()}</p>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="border-t border-gray-100 mt-6 pt-4">
              <div className="flex justify-between items-center">
                <span className="text-lg font-medium text-gray-900">Total</span>
                <span className="text-xl font-bold text-gray-900">Kshs. {order.total?.toLocaleString()}</span>
              </div>
            </div>
          </div>

          {/* Order Timeline */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-lg font-serif text-gray-900 mb-4">Order Timeline</h2>
            <div className="space-y-4">
              {getTimelineSteps().map((step, index) => (
                <div key={index} className="flex items-center gap-4">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    step.completed ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'
                  }`}>
                    {step.completed ? '✓' : index + 1}
                  </div>
                  <div className="flex-1">
                    <p className={`font-medium ${step.completed ? 'text-gray-900' : 'text-gray-500'}`}>
                      {step.status}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          
          {/* Order Status */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-medium text-gray-900 mb-4">Order Status</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">Current Status</span>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(currentStatus)}`}>
                  {currentStatus?.toUpperCase()}
                </span>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Update Status</label>
                <select
                  value={currentStatus}
                  onChange={(e) => updateOrderStatus(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                >
                  <option value="Paid">Paid</option>
                  <option value="Processing">Processing</option>
                  <option value="Shipped">Shipped</option>
                  <option value="Delivered">Delivered</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </div>
            </div>
          </div>

          {/* Customer Info */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-medium text-gray-900 mb-4">Customer Information</h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <User size={16} className="text-gray-400" />
                <div>
                  <p className="font-medium text-gray-900">{order.customer?.firstName} {order.customer?.lastName}</p>
                  <p className="text-sm text-gray-500">{order.customer?.email}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <MapPin size={16} className="text-gray-400" />
                <p className="text-sm text-gray-600">{order.customer?.address}, {order.customer?.city}</p>
              </div>
              
              <div className="flex items-center gap-3">
                <CreditCard size={16} className="text-gray-400" />
                <p className="text-sm text-gray-600">{order.customer?.paymentMethod || 'M-Pesa'}</p>
              </div>
              
              <div className="flex items-center gap-3">
                <Calendar size={16} className="text-gray-400" />
                <p className="text-sm text-gray-600">{new Date(order.createdAt).toLocaleDateString()}</p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-medium text-gray-900 mb-4">Actions</h3>
            <div className="space-y-3">
              <button
                onClick={generateInvoice}
                className="w-full flex items-center gap-2 px-4 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700 transition-colors"
              >
                <FileText size={16} />
                View Invoice
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderDetails;
