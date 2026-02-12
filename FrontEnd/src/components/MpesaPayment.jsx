import React, { useState } from 'react';
import { Smartphone, CheckCircle, XCircle, Loader } from 'lucide-react';
import { ordersAPI } from '../services/api';

const MpesaPayment = ({ amount, onSuccess, onCancel, userPhone = '', cartItems = [] }) => {
  const [phoneNumber, setPhoneNumber] = useState(userPhone);
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState(null); // 'success', 'failed', null
  const [errorMessage, setErrorMessage] = useState('');
  const [mpesaResponse, setMpesaResponse] = useState(null);

  const formatPhoneNumber = (value) => {
    // Remove non-digits
    const digits = value.replace(/\D/g, '');
    
    // Format as Kenyan number
    if (digits.startsWith('254')) {
      return digits.slice(0, 12);
    } else if (digits.startsWith('0')) {
      return '254' + digits.slice(1, 10);
    } else if (digits.startsWith('7') || digits.startsWith('1')) {
      return '254' + digits.slice(0, 9);
    }
    return digits.slice(0, 12);
  };

  const handlePhoneChange = (e) => {
    const formatted = formatPhoneNumber(e.target.value);
    setPhoneNumber(formatted);
  };

  const initiatePayment = async () => {
    if (phoneNumber.length < 12) {
      alert('Please enter a valid phone number');
      return;
    }

    setIsProcessing(true);
    setPaymentStatus(null);
    setErrorMessage('');

    try {
      // Call the real backend checkout endpoint with cart items
      const response = await ordersAPI.checkout(phoneNumber, cartItems);
      console.log('Checkout response:', response.data);
      
      setMpesaResponse(response.data);
      
      // Check if M-Pesa request was successful
      const mpesaStatus = response.data.mpesa_status;
      
      if (mpesaStatus?.ResponseCode === '0' || mpesaStatus?.CheckoutRequestID) {
        // STK Push sent successfully
        setPaymentStatus('success');
        
        setTimeout(() => {
          onSuccess({
            transactionId: mpesaStatus.CheckoutRequestID || `MPX${Date.now()}`,
            phoneNumber,
            amount,
            timestamp: new Date().toISOString(),
            orderDetails: response.data.order_details,
            orderId: response.data.order_id
          });
        }, 1500);
      } else if (mpesaStatus?.errorCode) {
        // M-Pesa error
        setPaymentStatus('failed');
        setErrorMessage(mpesaStatus.errorMessage || 'M-Pesa payment failed');
      } else {
        // Unexpected response
        setPaymentStatus('failed');
        setErrorMessage('Unexpected response from payment gateway');
      }
    } catch (error) {
      console.error('Checkout error:', error);
      setIsProcessing(false);
      setPaymentStatus('failed');
      setErrorMessage(
        error.response?.data?.detail || 
        error.response?.data?.message || 
        'Failed to initiate M-Pesa payment. Please try again.'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
          <Smartphone size={24} className="text-green-600" />
        </div>
        <div>
          <h3 className="text-lg font-serif text-gray-900">M-Pesa Payment</h3>
          <p className="text-sm text-gray-500">Pay with M-Pesa STK Push</p>
        </div>
      </div>

      {!paymentStatus && (
        <>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              M-Pesa Phone Number
            </label>
            <input
              type="tel"
              value={phoneNumber}
              onChange={handlePhoneChange}
              placeholder="254712345678"
              className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              disabled={isProcessing}
            />
            <p className="text-xs text-gray-500 mt-2">
              Enter your M-Pesa registered phone number
            </p>
          </div>

          <div className="bg-pink-50 rounded-xl p-4 mb-6 border border-pink-100">
            <div className="flex justify-between items-center">
              <span className="text-gray-700 font-medium">Total Amount</span>
              <span className="text-2xl font-bold text-gray-900">
                KES {amount.toLocaleString()}
              </span>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={onCancel}
              disabled={isProcessing}
              className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={initiatePayment}
              disabled={isProcessing || phoneNumber.length < 12}
              className="flex-1 px-6 py-3 bg-pink-600 text-white rounded-xl hover:bg-pink-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {isProcessing ? (
                <>
                  <Loader size={18} className="animate-spin" />
                  Processing...
                </>
              ) : (
                'Pay with M-Pesa'
              )}
            </button>
          </div>

          {isProcessing && (
            <div className="mt-4 p-4 bg-green-50 rounded-xl border border-green-200">
              <p className="text-sm text-green-800 text-center font-medium">
                ⏳ Sending STK Push to {phoneNumber}...
              </p>
              <p className="text-xs text-gray-600 text-center mt-2">
                Check your phone for the M-Pesa prompt and enter your PIN
              </p>
            </div>
          )}
        </>
      )}

      {paymentStatus === 'success' && (
        <div className="text-center py-6">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle size={32} className="text-green-600" />
          </div>
          <h4 className="text-lg font-medium text-gray-900 mb-2">Payment Successful!</h4>
          <p className="text-gray-600">Your order has been confirmed</p>
        </div>
      )}

      {paymentStatus === 'failed' && (
        <div className="text-center py-6">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <XCircle size={32} className="text-red-600" />
          </div>
          <h4 className="text-lg font-medium text-gray-900 mb-2">Payment Failed</h4>
          <p className="text-gray-600 mb-4">
            {errorMessage || 'The transaction was cancelled or failed'}
          </p>
          <button
            onClick={() => {
              setPaymentStatus(null);
              setErrorMessage('');
            }}
            className="px-6 py-2 bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-colors"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

export default MpesaPayment;
