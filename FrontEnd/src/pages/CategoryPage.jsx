import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProducts } from '../features/products/productsSlice';
import ProductCard from '../features/products/ProductCard';
import { Search, Filter, X } from 'lucide-react';

const CategoryPage = () => {
  const { category } = useParams();
  const dispatch = useDispatch();
  const { items: products } = useSelector((state) => state.products);
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchTerm, setSearchTerm] = useState(searchParams.get('search') || '');
  const [sortBy, setSortBy] = useState('name');
  const [priceRange, setPriceRange] = useState([0, 10000]);
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  useEffect(() => {
    const search = searchParams.get('search');
    if (search) {
      setSearchTerm(search);
    }
  }, [searchParams]);

  // Helper to normalize text (e.g., "skincare" matches "Skincare")
  const categoryName = category ? category.charAt(0).toUpperCase() + category.slice(1) : 'Shop All';

  // Filter and search products
  let displayProducts = category === 'shop' 
    ? products 
    : products.filter(p => p.category?.toLowerCase() === category?.toLowerCase());

  console.log('📊 Category:', category, '| Total products:', products.length, '| Filtered:', displayProducts.length);

  // Apply search filter
  if (searchTerm) {
    displayProducts = displayProducts.filter(product => 
      product.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.category?.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  // Apply price filter
  displayProducts = displayProducts.filter(product => 
    product.price >= priceRange[0] && product.price <= priceRange[1]
  );

  // Apply sorting
  displayProducts.sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'rating':
        return b.rating - a.rating;
      case 'name':
      default:
        return a.name.localeCompare(b.name);
    }
  });

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      setSearchParams({ search: searchTerm });
    } else {
      setSearchParams({});
    }
  };

  const clearSearch = () => {
    setSearchTerm('');
    setSearchParams({});
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">
          {searchTerm ? `Search Results for "${searchTerm}"` : categoryName}
        </h1>
        <p className="text-gray-500 max-w-2xl mx-auto">
          {searchTerm 
            ? `Found ${displayProducts.length} products matching your search`
            : `Explore our curated collection of premium ${categoryName} products. Designed to bring out your natural beauty.`
          }
        </p>
      </div>

      {/* Search and Filters */}
      <div className="mb-8 space-y-4">
        {/* Search Bar */}
        <form onSubmit={handleSearch} className="max-w-md mx-auto">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search products..."
              className="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent"
            />
            {searchTerm && (
              <button
                type="button"
                onClick={clearSearch}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <X size={18} />
              </button>
            )}
          </div>
        </form>

        {/* Filter Toggle and Sort */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-xl hover:bg-gray-50 transition-colors"
          >
            <Filter size={18} />
            Filters
          </button>
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent"
          >
            <option value="name">Sort by Name</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="rating">Highest Rated</option>
          </select>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Price Range</label>
                <div className="flex items-center gap-4">
                  <input
                    type="number"
                    value={priceRange[0]}
                    onChange={(e) => setPriceRange([parseInt(e.target.value) || 0, priceRange[1]])}
                    className="w-20 px-3 py-2 border border-gray-200 rounded-lg"
                    placeholder="Min"
                  />
                  <span className="text-gray-500">to</span>
                  <input
                    type="number"
                    value={priceRange[1]}
                    onChange={(e) => setPriceRange([priceRange[0], parseInt(e.target.value) || 10000])}
                    className="w-20 px-3 py-2 border border-gray-200 rounded-lg"
                    placeholder="Max"
                  />
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {displayProducts.length > 0 ? (
        <>
          <div className="mb-6 text-sm text-gray-500">
            Showing {displayProducts.length} of {products.length} products
          </div>
          
          {/* Group by category if searching */}
          {searchTerm ? (
            <div className="space-y-12">
              {['Skincare', 'Makeup', 'Haircare'].map(cat => {
                const categoryProducts = displayProducts.filter(p => p.category === cat);
                if (categoryProducts.length === 0) return null;
                
                return (
                  <div key={cat}>
                    <h3 className="text-xl font-serif text-gray-900 mb-6">{cat} ({categoryProducts.length})</h3>
                    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
                      {categoryProducts.map((product) => (
                        <ProductCard key={product.id} product={product} />
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {displayProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-20 bg-gray-50 rounded-xl border border-dashed border-gray-300">
          <h3 className="text-xl font-serif text-gray-400">
            {searchTerm ? 'No products found matching your search' : 'No products found in this category yet.'}
          </h3>
          <p className="text-gray-400 text-sm mt-2">
            {searchTerm ? 'Try adjusting your search terms or filters' : 'Check back soon for new arrivals!'}
          </p>
          {searchTerm && (
            <button
              onClick={clearSearch}
              className="mt-4 px-6 py-2 bg-pink-500 text-white rounded-xl hover:bg-pink-600 transition-colors"
            >
              Clear Search
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default CategoryPage;