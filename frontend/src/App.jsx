import { useState, useEffect } from 'react';
import './App.css';

// Simple icons as SVG components
const CartIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="9" cy="21" r="1"></circle>
    <circle cx="20" cy="21" r="1"></circle>
    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
  </svg>
);

const CloseIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18"></line>
    <line x1="6" y1="6" x2="18" y2="18"></line>
  </svg>
);

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // App State
  const [view, setView] = useState('home'); // 'home', 'checkout', 'success'
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [cart, setCart] = useState([]);
  
  // Checkout State
  const [formData, setFormData] = useState({
    name: '', email: '', address: '', city: '', zip_code: '', card_name: '', card_number: ''
  });
  const [orderResult, setOrderResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // Fetch Products
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // Assume API is running on localhost:8000
        const res = await fetch('http://localhost:8000/api/products');
        if (!res.ok) throw new Error('Failed to fetch products');
        const data = await res.json();
        setProducts(data);
      } catch (err) {
        console.error(err);
        setError('Unable to load products. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();

    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });
    setIsCartOpen(true);
  };

  const updateQuantity = (id, delta) => {
    setCart(prev => prev.map(item => {
      if (item.id === id) {
        const newQ = item.quantity + delta;
        return newQ > 0 ? { ...item, quantity: newQ } : item;
      }
      return item;
    }).filter(item => item.quantity > 0));
  };

  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const handleCheckout = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const orderData = {
      ...formData,
      items: cart.map(item => ({ id: item.id, name: item.name, price: item.price, quantity: item.quantity })),
      total_amount: cartTotal
    };

    try {
      const res = await fetch('http://localhost:8000/api/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
      
      const data = await res.json();
      if (res.ok) {
        setOrderResult(data);
        setCart([]);
        setView('success');
        setIsCartOpen(false);
      } else {
        const errorMsg = Array.isArray(data.detail)
          ? data.detail.map(err => `${err.loc[err.loc.length - 1]}: ${err.msg}`).join('\n')
          : (data.detail || 'Unknown error');
        alert('Checkout failed:\n' + errorMsg);
      }
    } catch (err) {
      alert('Error connecting to server.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Image Fallback Component
  const ProductImage = ({ src, name, className }) => {
    const [imgError, setImgError] = useState(false);
    if (imgError || !src) {
      return (
        <div className={`product-placeholder ${className || ''}`}>
          {name.substring(0, 2).toUpperCase()}
        </div>
      );
    }
    return <img src={src} alt={name} className={className} onError={() => setImgError(true)} />;
  };

  return (
    <>
      {/* Navbar */}
      <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
        <div className="logo" onClick={() => setView('home')} style={{cursor: 'pointer'}}>
          <div className="logo-icon">A</div>
          AURA
        </div>
        <div className="nav-links">
          <a href="#" className="nav-link" onClick={() => setView('home')}>Products</a>
          <button className="cart-btn" onClick={() => setIsCartOpen(true)}>
            <CartIcon />
            {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main>
        {view === 'home' && (
          <>
            <section className="hero">
              <div className="abstract-shape shape-1"></div>
              <div className="abstract-shape shape-2"></div>
              <div className="hero-content animate-fade-in">
                <h1>Experience <span className="text-gradient">Pure Audio</span> Perfection</h1>
                <p>Immerse yourself in studio-grade sound with our premium collection of audiophile gear. Crafted for those who hear the difference.</p>
                <button className="btn-primary" onClick={() => document.getElementById('products').scrollIntoView({behavior: 'smooth'})}>
                  Explore Collection
                </button>
              </div>
              <div className="hero-visual glass-panel animate-fade-in" style={{animationDelay: '0.2s', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                 {/* Decorative Hero Element */}
                 <div style={{
                   width: '200px', height: '200px', 
                   borderRadius: '50%', 
                   background: 'linear-gradient(135deg, var(--accent), var(--accent-purple))',
                   animation: 'pulse-glow 4s infinite alternate',
                   display: 'grid', placeItems: 'center', fontSize: '4rem', fontWeight: 'bold'
                 }}>AURA</div>
              </div>
            </section>

            <section id="products" className="products-section">
              <div className="section-header">
                <h2>Featured <span className="text-gradient">Products</span></h2>
              </div>
              
              {loading ? (
                <div style={{textAlign: 'center', padding: '50px'}}>Loading amazing gear...</div>
              ) : error ? (
                <div style={{textAlign: 'center', color: 'var(--danger)'}}>{error}</div>
              ) : (
                <div className="product-grid">
                  {products.map(product => (
                    <div key={product.id} className="product-card glass-panel" onClick={() => setSelectedProduct(product)}>
                      <div className="product-image-container">
                        <ProductImage src={product.image} name={product.name} className="product-image" />
                      </div>
                      <div className="product-info">
                        <div className="product-category">{product.category}</div>
                        <h3 className="product-name">{product.name}</h3>
                        <div className="product-price">
                          ${product.price.toFixed(2)}
                          <button className="btn-add" onClick={(e) => { e.stopPropagation(); addToCart(product); }}>+</button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}

        {view === 'checkout' && (
          <section className="checkout-view animate-fade-in">
            <h2 className="text-gradient" style={{marginBottom: '30px', fontSize: '2.5rem'}}>Complete Your Order</h2>
            <div className="glass-panel" style={{padding: '40px', borderRadius: '20px'}}>
              <form onSubmit={handleCheckout}>
                <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
                  <div className="form-group">
                    <label>Full Name</label>
                    <input required type="text" className="form-control" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Email Address</label>
                    <input required type="email" className="form-control" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
                  </div>
                </div>
                <div className="form-group">
                  <label>Shipping Address</label>
                  <input required type="text" className="form-control" value={formData.address} onChange={e => setFormData({...formData, address: e.target.value})} />
                </div>
                <div style={{display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px'}}>
                  <div className="form-group">
                    <label>City</label>
                    <input required type="text" className="form-control" value={formData.city} onChange={e => setFormData({...formData, city: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>ZIP Code</label>
                    <input required type="text" className="form-control" value={formData.zip_code} onChange={e => setFormData({...formData, zip_code: e.target.value})} />
                  </div>
                </div>
                
                <h3 style={{margin: '30px 0 15px', color: 'var(--accent)'}}>Mock Payment</h3>
                <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
                  <div className="form-group">
                    <label>Cardholder Name</label>
                    <input required type="text" className="form-control" placeholder="John Doe" value={formData.card_name} onChange={e => setFormData({...formData, card_name: e.target.value})} />
                  </div>
                  <div className="form-group">
                    <label>Card Number</label>
                    <input required type="text" className="form-control" placeholder="123456789012" minLength="12" maxLength="19" value={formData.card_number} onChange={e => setFormData({...formData, card_number: e.target.value})} />
                  </div>
                </div>

                <div style={{marginTop: '40px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                  <div style={{fontSize: '1.5rem'}}>Total: <strong>${cartTotal.toFixed(2)}</strong></div>
                  <button type="submit" className="btn-primary" disabled={isSubmitting}>
                    {isSubmitting ? 'Processing...' : 'Place Order'}
                  </button>
                </div>
              </form>
            </div>
          </section>
        )}

        {view === 'success' && orderResult && (
          <section className="order-success animate-fade-in">
            <div className="glass-panel" style={{padding: '50px', borderRadius: '20px'}}>
              <div className="success-icon">✓</div>
              <h2 style={{fontSize: '2.5rem', marginBottom: '15px'}}>Order Confirmed!</h2>
              <p style={{color: 'var(--text-secondary)', marginBottom: '30px'}}>Thank you for your purchase. Your audio journey begins soon.</p>
              <div style={{background: 'rgba(255,255,255,0.05)', padding: '20px', borderRadius: '12px', marginBottom: '40px'}}>
                <p>Order Reference: <strong className="text-gradient">{orderResult.order_id}</strong></p>
                <p>Amount Paid: <strong>${orderResult.total_amount.toFixed(2)}</strong></p>
              </div>
              <button className="btn-primary" onClick={() => setView('home')}>Return to Store</button>
            </div>
          </section>
        )}
      </main>

      {/* Product Details Modal */}
      {selectedProduct && (
        <div className="modal-overlay" onClick={() => setSelectedProduct(null)}>
          <div className="modal-content glass" onClick={e => e.stopPropagation()}>
            <button className="btn-close" onClick={() => setSelectedProduct(null)}><CloseIcon /></button>
            
            <div className="detail-image-container">
              <ProductImage src={selectedProduct.image} name={selectedProduct.name} />
            </div>
            
            <div className="detail-info">
              <div className="product-category">{selectedProduct.category}</div>
              <h2 className="detail-name">{selectedProduct.name}</h2>
              <p className="detail-tagline">{selectedProduct.tagline}</p>
              
              <div style={{display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px'}}>
                <span style={{color: '#ffd700'}}>★ {selectedProduct.rating}</span>
                <span style={{color: 'var(--text-secondary)'}}>({selectedProduct.reviews_count} reviews)</span>
              </div>
              
              <div className="detail-price">${selectedProduct.price.toFixed(2)}</div>
              <p className="detail-desc">{selectedProduct.description}</p>
              
              {selectedProduct.specs && (
                <div className="specs-grid">
                  {Object.entries(selectedProduct.specs).map(([key, val]) => (
                    <div key={key} className="spec-item">
                      <div className="spec-label">{key}</div>
                      <div className="spec-value">{val}</div>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="action-buttons">
                <button className="btn-primary btn-full" onClick={() => { addToCart(selectedProduct); setSelectedProduct(null); }}>
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Cart Drawer */}
      <div className={`cart-drawer ${isCartOpen ? 'open' : ''}`}>
        <div className="cart-header">
          <h3>Your Cart</h3>
          <button className="btn-close" style={{position: 'static', background: 'transparent'}} onClick={() => setIsCartOpen(false)}>
            <CloseIcon />
          </button>
        </div>
        
        {cart.length === 0 ? (
          <div style={{textAlign: 'center', marginTop: '50px', color: 'var(--text-secondary)'}}>
            Your cart is empty.
          </div>
        ) : (
          <>
            <div className="cart-items">
              {cart.map(item => (
                <div key={item.id} className="cart-item">
                  <div className="cart-item-img">
                    <ProductImage src={item.image} name={item.name} />
                  </div>
                  <div className="cart-item-details">
                    <div className="cart-item-name">{item.name}</div>
                    <div className="cart-item-price">${item.price.toFixed(2)}</div>
                    <div className="qty-controls">
                      <button className="qty-btn" onClick={() => updateQuantity(item.id, -1)}>-</button>
                      <span>{item.quantity}</span>
                      <button className="qty-btn" onClick={() => updateQuantity(item.id, 1)}>+</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="cart-footer">
              <div className="cart-total">
                <span>Total</span>
                <span className="text-gradient">${cartTotal.toFixed(2)}</span>
              </div>
              <button 
                className="btn-primary" 
                style={{width: '100%'}} 
                onClick={() => { setIsCartOpen(false); setView('checkout'); }}
              >
                Proceed to Checkout
              </button>
            </div>
          </>
        )}
      </div>
      
      {/* Overlay to close drawer */}
      {isCartOpen && <div style={{position: 'fixed', top:0, left:0, right:0, bottom:0, zIndex: 1000}} onClick={() => setIsCartOpen(false)}></div>}
    </>
  );
}

export default App;
