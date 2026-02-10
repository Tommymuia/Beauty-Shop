import React, { useState } from 'react';
import { Smartphone, CheckCircle, XCircle, Loader } from 'lucide-react';

const MpesaPayment = ({ amount, onSuccess, onCancel, userPhone = '' }) => {
  const [phoneNumber, setPhoneNumber] = useState(userPhone);
  const [isProcessing, setIsProcessing] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState(null); // 'success', 'failed', null

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

    // Real M-Pesa integration would go here
    // For now, simulate STK Push
    setTimeout(() => {
      const success = Math.random() > 0.2;
      
      setIsProcessing(false);
      setPaymentStatus(success ? 'success' : 'failed');
      
      if (success) {
        setTimeout(() => {
          onSuccess({
            transactionId: `MPX${Date.now()}`,
            phoneNumber,
            amount,
            timestamp: new Date().toISOString()
          });
        }, 1500);
      }
    }, 3000);
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
            <div className="mt-4 p-4 bg-pink-50 rounded-xl border border-pink-100">
              <p className="text-sm text-pink-800 text-center">
                Please check your phone for the M-Pesa prompt and enter your PIN
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
          <p className="text-gray-600 mb-4">The transaction was cancelled or failed</p>
          <button
            onClick={() => {
              setPaymentStatus(null);
              setPhoneNumber('');
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
