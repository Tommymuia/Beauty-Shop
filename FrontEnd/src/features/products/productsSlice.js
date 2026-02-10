import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { productsAPI } from '../../services/api';
import { products as fakeProducts } from '../../services/fakeData';

const initialState = {
  items: fakeProducts, // Start with fake data as fallback
  currentProduct: null,
  isLoading: false,
  error: null,
  useBackend: false, // Flag to switch between fake and real data
};

// Async thunks
export const fetchProducts = createAsyncThunk(
  'products/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      console.log('🔄 Fetching products from API...');
      const response = await productsAPI.getAll(params);
      console.log('✅ API Response:', response.data.length, 'products');
      return response.data;
    } catch (error) {
      console.error('❌ API Error:', error);
      // Fallback to fake data on error
      return rejectWithValue(error.response?.data?.detail || 'Using local data');
    }
  }
);

export const fetchProductById = createAsyncThunk(
  'products/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await productsAPI.getById(id);
      return response.data;
    } catch (error) {
      // Fallback to fake data
      const product = fakeProducts.find(p => p.id === parseInt(id));
      if (product) return product;
      return rejectWithValue(error.response?.data?.detail || 'Product not found');
    }
  }
);

const productsSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {
    clearCurrentProduct(state) {
      state.currentProduct = null;
    },
    clearError(state) {
      state.error = null;
    },
    setUseBackend(state, action) {
      state.useBackend = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = action.payload.length > 0 ? action.payload : fakeProducts;
        state.useBackend = action.payload.length > 0;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
        state.items = fakeProducts; // Use fake data on error
        state.useBackend = false;
      })
      .addCase(fetchProductById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProductById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentProduct = action.payload;
      })
      .addCase(fetchProductById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearCurrentProduct, clearError, setUseBackend } = productsSlice.actions;
export default productsSlice.reducer;
