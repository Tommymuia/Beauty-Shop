// Adapter to transform between frontend and backend data formats

// Category mapping
const CATEGORY_MAP = {
  'Skincare': 1,
  'Haircare': 2,
  'Makeup': 3
};

const CATEGORY_REVERSE_MAP = {
  1: 'Skincare',
  2: 'Haircare',
  3: 'Makeup'
};

// Transform backend product to frontend format
export const transformProductFromBackend = (backendProduct) => {
  return {
    id: backendProduct.id,
    name: backendProduct.name,
    description: backendProduct.description || '',
    price: backendProduct.price,
    category: CATEGORY_REVERSE_MAP[backendProduct.category_id] || 'Skincare',
    stock: backendProduct.stock_quantity || 0,
    image: backendProduct.image || 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&q=80&w=600',
    rating: backendProduct.rating || 4.5,
    isNew: backendProduct.is_new || false,
    reviews: backendProduct.reviews || 0
  };
};

// Transform frontend product to backend format
export const transformProductToBackend = (frontendProduct) => {
  return {
    name: frontendProduct.name,
    description: frontendProduct.description,
    price: parseFloat(frontendProduct.price),
    category_id: CATEGORY_MAP[frontendProduct.category] || 1,
    stock_quantity: parseInt(frontendProduct.stock) || 0
  };
};

// Transform cart item from backend
export const transformCartItemFromBackend = (backendItem) => {
  return {
    id: backendItem.id,
    productId: backendItem.product_id,
    quantity: backendItem.quantity,
    product: backendItem.product ? transformProductFromBackend(backendItem.product) : null,
    price: backendItem.product?.price || 0,
    totalPrice: (backendItem.product?.price || 0) * backendItem.quantity
  };
};

// Transform order from backend
export const transformOrderFromBackend = (backendOrder) => {
  return {
    id: backendOrder.id,
    invoiceNumber: backendOrder.invoice_number,
    total: backendOrder.total_amount,
    status: backendOrder.status,
    createdAt: backendOrder.created_at,
    billingAddress: backendOrder.billing_address
  };
};

export default {
  transformProductFromBackend,
  transformProductToBackend,
  transformCartItemFromBackend,
  transformOrderFromBackend
};
