import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchUserOrders } from './ordersSlice';
import { Package, Eye, Calendar, CreditCard } from 'lucide-react';

const OrderHistory = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { orders, isLoading } = useSelector((state) => state.orders);

  useEffect(() => {
    dispatch(fetchUserOrders());
  }, [dispatch]);

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-12 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
        <p className="mt-4 text-gray-500">Loading your orders...</p>
      </div>
    );
  }

  if (!orders || orders.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-12 text-center">
        <Package size={64} className="mx-auto text-gray-300 mb-4" />
        <h2 className="text-2xl font-serif text-gray-900 mb-2">No Orders Yet</h2>
        <p className="text-gray-500 mb-6">Start shopping to see your order history here</p>
        <button
          onClick={() => navigate('/')}
          className="px-6 py-3 bg-pink-600 text-white rounded-full font-medium hover:bg-pink-700 transition-colors"
        >
          Start Shopping
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <h1 className="text-3xl font-serif text-gray-900 mb-8">Order History</h1>
      
      <div className="space-y-4">
        {orders.map((order) => (
          <div
            key={order.id}
            className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="font-bold text-lg text-gray-900">
                  Order #{order.invoice_number || order.id}
                </h3>
                <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                  <div className="flex items-center gap-1">
                    <Calendar size={16} />
                    <span>{new Date(order.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <CreditCard size={16} />
                    <span>Kshs. {order.total_amount?.toLocaleString()}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-3">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  order.status === 'completed' ? 'bg-green-100 text-green-800' :
                  order.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                  order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {order.status?.toUpperCase()}
                </span>
                
                <button
                  onClick={() => navigate(`/invoice/${order.id}`)}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <Eye size={16} />
                  View Invoice
                </button>
              </div>
            </div>
            
            {/* Order Items Preview */}
            {order.items_json && (
              <div className="border-t border-gray-100 pt-4 mt-4">
                <p className="text-sm text-gray-500 mb-2">Items:</p>
                <div className="flex flex-wrap gap-2">
                  {JSON.parse(order.items_json).slice(0, 3).map((item, idx) => (
                    <span key={idx} className="text-xs bg-gray-100 px-2 py-1 rounded">
                      {item.name} x{item.quantity}
                    </span>
                  ))}
                  {JSON.parse(order.items_json).length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{JSON.parse(order.items_json).length - 3} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default OrderHistory;
