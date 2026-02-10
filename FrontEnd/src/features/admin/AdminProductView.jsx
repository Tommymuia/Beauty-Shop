import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Edit, Star, Package, DollarSign } from 'lucide-react';
import { productsAPI } from '../../services/api';

const AdminProductView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await productsAPI.getById(id);
        setProduct(response.data);
      } catch (error) {
        console.error('Error fetching product:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Product not found</p>
        <button onClick={() => navigate('/admin/products')} className="mt-4 text-pink-600 hover:text-pink-700">
          Back to Products
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/admin/products')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft size={20} />
          Back to Products
        </button>
        <Link
          to={`/admin/products/edit/${product.id}`}
          className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-xl hover:bg-gray-800 transition-colors"
        >
          <Edit size={18} />
          Edit Product
        </Link>
      </div>

      {/* Product Details */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
          {/* Image */}
          <div className="relative aspect-square bg-gray-100 rounded-xl overflow-hidden">
            <img 
              src={product.image} 
              alt={product.name}
              className="w-full h-full object-cover"
            />
            {product.isNew && (
              <span className="absolute top-4 left-4 bg-pink-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                NEW
              </span>
            )}
          </div>

          {/* Info */}
          <div className="space-y-6">
            <div>
              <span className="text-sm text-gray-500">{product.category}</span>
              <h1 className="text-3xl font-serif text-gray-900 mt-1">{product.name}</h1>
            </div>

            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <Star size={20} className="text-yellow-400 fill-current" />
                <span className="text-lg font-medium">{product.rating}</span>
              </div>
              <div className="flex items-center gap-2">
                <Package size={20} className="text-gray-400" />
                <span className="text-lg">{product.stock} in stock</span>
              </div>
            </div>

            <div className="flex items-baseline gap-2">
              <DollarSign size={24} className="text-gray-400" />
              <span className="text-4xl font-bold text-gray-900">Kshs. {product.price.toLocaleString()}</span>
            </div>

            <div className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${
              product.stock > 20 
                ? 'bg-green-100 text-green-800' 
                : product.stock > 5 
                ? 'bg-yellow-100 text-yellow-800'
                : 'bg-red-100 text-red-800'
            }`}>
              {product.stock > 20 ? 'In Stock' : product.stock > 5 ? 'Low Stock' : 'Very Low Stock'}
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Description</h3>
              <p className="text-gray-600 leading-relaxed">{product.description}</p>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <dl className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt className="text-gray-500">Product ID</dt>
                  <dd className="font-medium text-gray-900">#{product.id}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">Category ID</dt>
                  <dd className="font-medium text-gray-900">{product.category_id}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminProductView;
