import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { clearCart } from '../cart/cartSlice';
import { createOrder } from './ordersSlice';
import { Loader2, Phone, CreditCard } from 'lucide-react';
import Notification from '../../components/Notification';
import MpesaPayment from '../../components/MpesaPayment';

const Checkout = () => {
  const { items, totalAmount } = useSelector((state) => state.cart);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('card');
  const [showMpesaModal, setShowMpesaModal] = useState(false);
  const [mpesaTransaction, setMpesaTransaction] = useState(null);
  const [notification, setNotification] = useState({ isVisible: false, message: '', type: 'info' });

  const [formData, setFormData] = useState({
    firstName: '', lastName: '', email: '', address: '', city: '', zip: '', card: ''
  });

  // Redirect if cart is empty - MUST be at top level
  React.useEffect(() => {
    if (items.length === 0) {
      navigate('/cart');
    }
  }, [items.length, navigate]);

  if (items.length === 0) {
    return null;
  }

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value });
  };

  const showNotification = (message, type = 'info') => {
    setNotification({ isVisible: true, message, type });
  };

  const hideNotification = () => {
    setNotification({ ...notification, isVisible: false });
  };

  const handleMpesaSuccess = (transaction) => {
    setMpesaTransaction(transaction);
    setShowMpesaModal(false);
    showNotification('M-Pesa payment successful!', 'success');
    // Auto-submit the order
    setTimeout(() => {
      handleSubmit(null, transaction);
    }, 1000);
  };

  const handleSubmit = async (e, mpesaData = null) => {
    if (e) e.preventDefault();
    
    // If M-Pesa selected and no transaction yet, show modal
    if (paymentMethod === 'mpesa' && !mpesaData && !mpesaTransaction) {
      console.log('Opening M-Pesa modal...');
      setShowMpesaModal(true);
      return;
    }
    
    setIsProcessing(true);

    const transaction = mpesaData || mpesaTransaction;
    const orderPayload = {
      customer: formData,
      items: items,
      total: totalAmount,
      paymentMethod: paymentMethod,
      ...(paymentMethod === 'mpesa' && transaction && { 
        mpesaPhone: transaction.phoneNumber,
        transactionId: transaction.transactionId 
      })
    };

    try {
      // Create order via API
      const result = await dispatch(createOrder(orderPayload)).unwrap();
      
      // Navigate to Order Confirmation page FIRST (before clearing cart to avoid redirect)
      navigate(`/order-confirmation/${result.id}`);
      
      // Clear Redux Cart after navigation
      setTimeout(() => dispatch(clearCart()), 100);
      
    } catch (error) {
      console.error("Checkout failed", error);
      showNotification(error || "Something went wrong. Please try again.", 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-12">
      <Notification 
        type={notification.type}
        message={notification.message}
        isVisible={notification.isVisible}
        onClose={hideNotification}
      />
      <h1 className="text-3xl font-serif text-gray-900 mb-8 text-center">Checkout</h1>
      
      <div className="grid md:grid-cols-2 gap-12">
        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <h3 className="font-bold text-lg">Shipping Details</h3>
          <div className="grid grid-cols-2 gap-4">
            <input required name="firstName" placeholder="First Name" onChange={handleChange} className="border p-3 rounded-lg w-full" />
            <input required name="lastName" placeholder="Last Name" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          </div>
          <input required name="email" type="email" placeholder="Email Address" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          <input required name="address" placeholder="Shipping Address" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          <div className="grid grid-cols-2 gap-4">
            <input required name="city" placeholder="City" onChange={handleChange} className="border p-3 rounded-lg w-full" />
            <input required name="zip" placeholder="Zip Code" onChange={handleChange} className="border p-3 rounded-lg w-full" />
          </div>

          <h3 className="font-bold text-lg pt-4">Payment Method</h3>
          
          {/* Payment Method Selection */}
          <div className="space-y-4">
            <div className="flex gap-4">
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="paymentMethod"
                  value="card"
                  checked={paymentMethod === 'card'}
                  onChange={(e) => setPaymentMethod(e.target.value)}
                  className="mr-2"
                />
                <CreditCard size={20} className="mr-2 text-gray-600" />
                <span>Credit/Debit Card</span>
              </label>
              
              <label className="flex items-center cursor-pointer">
                <input
                  type="radio"
                  name="paymentMethod"
                  value="mpesa"
                  checked={paymentMethod === 'mpesa'}
                  onChange={(e) => setPaymentMethod(e.target.value)}
                  className="mr-2"
                />
                <Phone size={20} className="mr-2 text-green-600" />
                <span>M-Pesa</span>
              </label>
            </div>

            {/* Card Payment */}
            {paymentMethod === 'card' && (
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <p className="text-sm text-gray-500 mb-2">Simulated Payment Gateway</p>
                <input 
                  required 
                  name="card" 
                  type="text" 
                  maxLength="19" 
                  placeholder="Card Number (XXXX XXXX XXXX XXXX)" 
                  onChange={handleChange}
                  className="border p-3 rounded-lg w-full bg-white" 
                />
              </div>
            )}

            {/* M-Pesa Payment */}
            {paymentMethod === 'mpesa' && (
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <p className="text-sm text-green-700 mb-3 font-medium">Pay with M-Pesa</p>
                {mpesaTransaction ? (
                  <div className="text-center py-3">
                    <span className="text-green-700 font-medium">✓ Payment Confirmed</span>
                    <p className="text-xs text-gray-600 mt-1">Transaction: {mpesaTransaction.transactionId}</p>
                  </div>
                ) : (
                  <>
                    <p className="text-sm text-gray-600 mb-3">Click "Pay with M-Pesa" below to complete payment</p>
                    <button
                      type="button"
                      onClick={() => {
                        console.log('Test button clicked');
                        setShowMpesaModal(true);
                      }}
                      className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
                    >
                      Open M-Pesa Payment
                    </button>
                  </>
                )}
              </div>
            )}
          </div>

          <button 
            type="submit" 
            disabled={isProcessing}
            className="w-full bg-pink-600 text-white py-4 rounded-full font-bold hover:bg-pink-700 transition shadow-lg mt-4 disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center"
          >
            {isProcessing ? (
              <><Loader2 className="animate-spin mr-2" /> Processing...</>
            ) : paymentMethod === 'mpesa' && !mpesaTransaction ? (
              'Pay with M-Pesa'
            ) : (
              `Complete Order - Kshs. ${totalAmount.toLocaleString()}`
            )}
          </button>
        </form>

        {/* Order Preview */}
        <div className="bg-gray-50 p-8 rounded-2xl h-fit">
          <h3 className="font-serif text-lg mb-4">Your Order</h3>
          <div className="space-y-3 mb-4 max-h-64 overflow-y-auto">
            {items.map(item => (
              <div key={item.id} className="flex justify-between text-sm">
                <span>{item.name} <span className="text-gray-400">x{item.quantity}</span></span>
                <span className="font-bold">Kshs. {item.totalPrice.toLocaleString()}</span>
              </div>
            ))}
          </div>
          <div className="border-t border-gray-200 pt-4 flex justify-between font-bold text-lg">
            <span>Total</span>
            <span>Kshs. {totalAmount.toLocaleString()}</span>
          </div>
        </div>
      </div>

      {/* M-Pesa Payment Modal */}
      {showMpesaModal && (
        <div className="fixed inset-0 bg-gradient-to-br from-pink-50 to-white flex items-center justify-center z-50 p-4">
          <div className="max-w-md w-full">
            <MpesaPayment
              amount={totalAmount}
              onSuccess={handleMpesaSuccess}
              onCancel={() => setShowMpesaModal(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Checkout;