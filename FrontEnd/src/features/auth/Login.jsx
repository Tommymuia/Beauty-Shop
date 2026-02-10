import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { Eye, EyeOff, Mail, Lock, ArrowLeft } from 'lucide-react';
import { loginSuccess, loginUser } from './authSlice';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    userType: 'customer'
  });
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { isLoading, error } = useSelector((state) => state.auth);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const result = await dispatch(loginUser({ 
        email: formData.email, 
        password: formData.password 
      })).unwrap();
      
      // Navigate based on user role
      if (result.is_admin) {
        navigate('/admin');
      } else {
        navigate('/');
      }
    } catch (error) {
      // Error is handled by Redux slice
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-white flex items-center justify-center px-6 py-12">
      <div className="max-w-md w-full">
        
        {/* Back Button */}
        <button 
          onClick={() => navigate('/')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft size={20} />
          <span>Back to Shop</span>
        </button>
        
        {/* Header */}
        <div className="text-center mb-8">
          <Link to="/" className="text-3xl font-serif font-bold tracking-tighter text-gray-900 mb-2 inline-block">
            Bloom Beauty<span className="text-pink-600">.</span>
          </Link>
          <h2 className="text-2xl font-serif text-gray-900 mb-2">Welcome Back</h2>
          <p className="text-gray-500">Sign in to your account to continue</p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* User Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Login as</label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setFormData({...formData, userType: 'customer'})}
                  className={`p-3 border-2 rounded-xl text-sm font-medium transition-all ${
                    formData.userType === 'customer'
                      ? 'border-pink-500 bg-pink-50 text-pink-700'
                      : 'border-gray-200 text-gray-600 hover:border-gray-300'
                  }`}
                >
                  Customer
                </button>
                <button
                  type="button"
                  onClick={() => setFormData({...formData, userType: 'admin'})}
                  className={`p-3 border-2 rounded-xl text-sm font-medium transition-all ${
                    formData.userType === 'admin'
                      ? 'border-pink-500 bg-pink-50 text-pink-700'
                      : 'border-gray-200 text-gray-600 hover:border-gray-300'
                  }`}
                >
                  Admin
                </button>
              </div>
            </div>
            
            {/* Email Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all"
                  placeholder="Enter your email"
                  required
                />
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">
                {error}
              </div>
            )}

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full pl-12 pr-12 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all"
                  placeholder="Enter your password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="w-4 h-4 text-pink-600 border-gray-300 rounded focus:ring-pink-500" />
                <span className="ml-2 text-sm text-gray-600">Remember me</span>
              </label>
              <Link to="/forgot-password" className="text-sm text-pink-600 hover:text-pink-700 font-medium">
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gray-900 text-white py-3 rounded-xl font-medium hover:bg-gray-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          {/* Divider */}
          {formData.userType === 'customer' && (
            <div className="mt-6 text-center">
              <span className="text-gray-500 text-sm">
                Don't have an account?{' '}
                <Link to="/register" className="text-pink-600 hover:text-pink-700 font-medium">
                  Sign up
                </Link>
              </span>
            </div>
          )}
          {formData.userType === 'admin' && (
            <div className="mt-6 text-center">
              <span className="text-gray-500 text-sm">
                Admin Personnel Only
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;