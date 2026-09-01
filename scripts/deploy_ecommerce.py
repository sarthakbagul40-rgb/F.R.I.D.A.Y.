import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAISON NOIR — Bespoke Luxury Footwear</title>
    <meta name="description" content="MAISON NOIR — Curated high-fashion luxury footwear, limited runs, hand-stitched Italian leather.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@500;600;700;800&display=swap" rel="stylesheet">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        gold: '#E5C07B',
                        'gold-light': '#F3DCAE',
                        dark: '#0B0F17',
                        'dark-card': '#121824',
                        'dark-border': 'rgba(255, 255, 255, 0.08)'
                    },
                    fontFamily: {
                        syne: ['Syne', 'sans-serif'],
                        sans: ['Plus Jakarta Sans', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body {
            background-color: #0B0F17;
            color: #EEF1F7;
            font-family: 'Plus Jakarta Sans', sans-serif;
            overflow-x: hidden;
        }
        .grain {
            position: fixed;
            inset: 0;
            z-index: 999;
            pointer-events: none;
            opacity: 0.04;
            mix-blend-mode: overlay;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        }
        .gold-gradient {
            background: linear-gradient(135deg, #E5C07B 0%, #F3DCAE 50%, #C9A253 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .card-spotlight {
            background: radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(229, 192, 123, 0.08), transparent 40%), #121824;
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.4s ease;
        }
        .card-spotlight:hover {
            transform: translateY(-6px);
            border-color: rgba(229, 192, 123, 0.35);
        }
        .drawer-slide {
            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
    </style>
</head>
<body class="antialiased selection:bg-gold selection:text-dark">
    <div class="grain"></div>

    <!-- Announcement Bar -->
    <div class="bg-gradient-to-r from-indigo-950/60 via-purple-950/60 to-indigo-950/60 border-b border-dark-border py-2 text-center text-xs tracking-widest uppercase font-semibold text-gray-300">
        ✨ Atelier Edition — Complimentary Worldwide Express Delivery & Custom Dust Bag
    </div>

    <!-- Navbar -->
    <nav class="sticky top-0 z-50 bg-dark/80 backdrop-blur-xl border-b border-dark-border">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                    <i data-lucide="gem" class="w-5 h-5 text-white"></i>
                </div>
                <div>
                    <span class="font-syne text-xl font-bold tracking-wider gold-gradient">MAISON NOIR</span>
                    <span class="block text-[9px] tracking-[0.3em] uppercase text-gray-400 font-semibold">Paris Atelier</span>
                </div>
            </div>

            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-gray-300">
                <a href="#collection" class="hover:text-gold transition-colors">Collection</a>
                <a href="#atelier" class="hover:text-gold transition-colors">Craftsmanship</a>
                <a href="#reviews" class="hover:text-gold transition-colors">Reviews</a>
            </div>

            <div class="flex items-center gap-4">
                <button onclick="toggleCart()" class="relative p-3 rounded-xl bg-white/5 border border-white/10 hover:border-gold transition-all text-gray-300 hover:text-gold">
                    <i data-lucide="shopping-bag" class="w-5 h-5"></i>
                    <span id="cart-badge" class="absolute -top-1.5 -right-1.5 min-w-[20px] h-5 px-1 bg-gold text-dark text-[11px] font-bold rounded-full flex items-center justify-center">0</span>
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <header class="relative pt-12 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto overflow-hidden">
        <div class="grid lg:grid-cols-12 gap-12 items-center">
            <div class="lg:col-span-7">
                <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-gold/10 border border-gold/30 text-gold text-xs font-semibold tracking-wider uppercase mb-6">
                    <span class="w-2 h-2 rounded-full bg-gold animate-pulse"></span>
                    Autumn / Winter Collection 2026
                </div>
                <h1 class="font-syne text-5xl sm:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6">
                    Sculpted for <br>
                    <span class="gold-gradient">Elegance & Power.</span>
                </h1>
                <p class="text-gray-400 text-lg sm:text-xl max-w-xl leading-relaxed mb-8">
                    Limited-edition silhouettes forged in full-grain Tuscan calfskin, Vibram technical outsoles, and hand-burnished finishes.
                </p>
                <div class="flex flex-wrap gap-4 items-center">
                    <a href="#collection" class="px-8 py-4 rounded-full bg-gradient-to-r from-gold to-gold-light text-dark font-bold text-sm tracking-wider uppercase hover:opacity-95 transition-opacity shadow-lg shadow-gold/20 flex items-center gap-2">
                        <span>Explore Collection</span>
                        <i data-lucide="arrow-down" class="w-4 h-4"></i>
                    </a>
                    <button onclick="showToast('Authenticity Certificate Included with every serial-numbered pair.')" class="px-8 py-4 rounded-full bg-white/5 border border-white/10 hover:border-gold/50 text-white font-medium text-sm transition-all flex items-center gap-2">
                        <i data-lucide="shield-check" class="w-4 h-4 text-gold"></i>
                        <span>100% Certified Original</span>
                    </button>
                </div>
            </div>

            <div class="lg:col-span-5 relative">
                <div class="relative rounded-3xl overflow-hidden border border-dark-border bg-gradient-to-b from-white/5 to-transparent p-4 shadow-2xl">
                    <img src="https://images.unsplash.com/photo-1552346154-21d32810aba3?q=80&w=1200&auto=format&fit=crop" alt="Hero Sneaker" class="rounded-2xl w-full h-[440px] object-cover hover:scale-105 transition-transform duration-700">
                    <div class="absolute bottom-8 left-8 right-8 bg-dark/85 backdrop-blur-md p-4 rounded-2xl border border-white/10 flex items-center justify-between">
                        <div>
                            <div class="text-xs text-gold uppercase tracking-wider font-semibold">Flagship Model</div>
                            <div class="font-syne text-lg font-bold">Noir Phantom High 01</div>
                            <div class="text-gray-400 text-sm font-semibold">$580 USD</div>
                        </div>
                        <button onclick="addToCart('Noir Phantom High 01', 580, 'https://images.unsplash.com/photo-1552346154-21d32810aba3?q=80&w=400&auto=format&fit=crop')" class="p-3 rounded-xl bg-gold text-dark hover:bg-gold-light transition-colors">
                            <i data-lucide="plus" class="w-5 h-5"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Product Collection Grid -->
    <section id="collection" class="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-dark-border">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
            <div>
                <span class="text-xs tracking-[0.25em] uppercase text-gold font-bold">Bespoke Catalog</span>
                <h2 class="font-syne text-4xl sm:text-5xl font-bold tracking-tight mt-2">Curated Silhouettes</h2>
            </div>
            <div class="flex gap-2 p-1 bg-white/5 rounded-full border border-white/10 w-fit">
                <button class="px-5 py-2 rounded-full bg-gold text-dark font-bold text-xs">All Pieces</button>
                <button class="px-5 py-2 rounded-full text-gray-400 hover:text-white font-medium text-xs">High-Tops</button>
                <button class="px-5 py-2 rounded-full text-gray-400 hover:text-white font-medium text-xs">Runners</button>
            </div>
        </div>

        <div id="product-grid" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Rendered by JS -->
        </div>
    </section>

    <!-- Atelier Heritage -->
    <section id="atelier" class="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto border-t border-dark-border">
        <div class="grid md:grid-cols-3 gap-8 text-center md:text-left">
            <div class="p-8 rounded-3xl bg-dark-card border border-dark-border">
                <div class="w-12 h-12 rounded-2xl bg-gold/10 text-gold flex items-center justify-center mb-6">
                    <i data-lucide="feather" class="w-6 h-6"></i>
                </div>
                <h3 class="font-syne text-xl font-bold mb-2">Italian Tuscan Leather</h3>
                <p class="text-gray-400 text-sm leading-relaxed">Full-grain hides naturally vegetable-tanned in Florence for unprecedented softness and patina over time.</p>
            </div>
            <div class="p-8 rounded-3xl bg-dark-card border border-dark-border">
                <div class="w-12 h-12 rounded-2xl bg-gold/10 text-gold flex items-center justify-center mb-6">
                    <i data-lucide="layers" class="w-6 h-6"></i>
                </div>
                <h3 class="font-syne text-xl font-bold mb-2">Vibram Megagrip Sole</h3>
                <p class="text-gray-400 text-sm leading-relaxed">Engineered composite rubber outsoles delivering cloud-level shock absorption and all-terrain traction.</p>
            </div>
            <div class="p-8 rounded-3xl bg-dark-card border border-dark-border">
                <div class="w-12 h-12 rounded-2xl bg-gold/10 text-gold flex items-center justify-center mb-6">
                    <i data-lucide="award" class="w-6 h-6"></i>
                </div>
                <h3 class="font-syne text-xl font-bold mb-2">Numbered Serial Edition</h3>
                <p class="text-gray-400 text-sm leading-relaxed">Each release is strictly capped at 500 hand-numbered pairs worldwide. Never re-issued.</p>
            </div>
        </div>
    </section>

    <!-- Slide-Out Cart Drawer -->
    <div id="cart-drawer-overlay" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm opacity-0 pointer-events-none transition-opacity duration-300" onclick="toggleCart()"></div>
    <div id="cart-drawer" class="fixed top-0 right-0 bottom-0 z-50 w-full max-w-md bg-dark-card border-l border-dark-border p-6 flex flex-col justify-between translate-x-full drawer-slide shadow-2xl">
        <div>
            <div class="flex items-center justify-between pb-4 border-b border-dark-border">
                <div class="flex items-center gap-2">
                    <i data-lucide="shopping-bag" class="w-5 h-5 text-gold"></i>
                    <h3 class="font-syne text-lg font-bold">Your Order Bag</h3>
                </div>
                <button onclick="toggleCart()" class="p-2 rounded-lg hover:bg-white/5 text-gray-400 hover:text-white">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <div id="cart-items" class="py-4 space-y-4 max-h-[60vh] overflow-y-auto">
                <p class="text-gray-500 text-sm text-center py-8">Your bag is currently empty.</p>
            </div>
        </div>

        <div class="pt-4 border-t border-dark-border space-y-4">
            <div class="flex justify-between text-sm">
                <span class="text-gray-400">Subtotal</span>
                <span id="cart-subtotal" class="font-bold text-white">$0.00</span>
            </div>
            <div class="flex justify-between text-sm">
                <span class="text-gray-400">Shipping</span>
                <span class="text-gold font-medium">Complimentary</span>
            </div>
            <button onclick="checkout()" class="w-full py-4 rounded-xl bg-gradient-to-r from-gold to-gold-light text-dark font-bold text-sm tracking-wider uppercase hover:opacity-95 transition-opacity shadow-lg shadow-gold/20 flex items-center justify-center gap-2">
                <span>Secure Checkout</span>
                <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </button>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 right-6 z-50 px-5 py-3.5 rounded-2xl bg-dark-card border border-gold/40 text-white text-sm shadow-2xl flex items-center gap-3 translate-y-20 opacity-0 transition-all duration-300">
        <i data-lucide="check-circle" class="w-5 h-5 text-gold"></i>
        <span id="toast-msg">Item added to bag.</span>
    </div>

    <!-- Footer -->
    <footer class="py-12 border-t border-dark-border text-center text-xs text-gray-500">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="font-syne font-bold text-gray-400">MAISON NOIR ATELIER © 2026</div>
            <div class="flex gap-6 text-gray-400">
                <a href="#" class="hover:text-gold">Privacy Protocol</a>
                <a href="#" class="hover:text-gold">Terms of Concierge</a>
                <a href="#" class="hover:text-gold">Worldwide Shipping</a>
            </div>
        </div>
    </footer>

    <script>
        const products = [
            {
                id: 1,
                name: "Aero Monaco Velvet Runner",
                tag: "Limited Release",
                price: 490,
                image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=600&auto=format&fit=crop",
                desc: "Burgundy Italian suede with aerated knit tongue and gold eyelets."
            },
            {
                id: 2,
                name: "Noir Obsidian High-Top",
                tag: "Atelier Special",
                price: 580,
                image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?q=80&w=600&auto=format&fit=crop",
                desc: "Matte black pebble calfskin, titanium lace locks, and Vibram chassis."
            },
            {
                id: 3,
                name: "Palais Royal Saffron Low",
                tag: "Trending",
                price: 460,
                image: "https://images.unsplash.com/photo-1608231387042-66d1773070a5?q=80&w=600&auto=format&fit=crop",
                desc: "Hand-patinated amber leather with raw edges and waxed cotton laces."
            },
            {
                id: 4,
                name: "St. Germain Minimalist White",
                tag: "Pure Essential",
                price: 420,
                image: "https://images.unsplash.com/photo-1560769629-975ec94e6a86?q=80&w=600&auto=format&fit=crop",
                desc: "Ultra-clean optic white calfskin with calf leather lining."
            },
            {
                id: 5,
                name: "Vanguard Cyber Carbon Pro",
                tag: "Performance Lux",
                price: 620,
                image: "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?q=80&w=600&auto=format&fit=crop",
                desc: "Carbon fiber shank plate, reflective piping, and kinetic foam cushioning."
            },
            {
                id: 6,
                name: "Venetian Emerald Court",
                tag: "Seasonal Excl.",
                price: 510,
                image: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?q=80&w=600&auto=format&fit=crop",
                desc: "Deep pine green tumbled leather with antique brass branding."
            }
        ];

        let cart = [];

        function renderProducts() {
            const container = document.getElementById('product-grid');
            container.innerHTML = products.map(p => `
                <div class="card-spotlight rounded-3xl p-5 border border-dark-border flex flex-col justify-between group">
                    <div>
                        <div class="relative rounded-2xl overflow-hidden aspect-square mb-5 bg-dark/50">
                            <img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                            <span class="absolute top-3 left-3 px-3 py-1 rounded-full bg-dark/80 backdrop-blur-md text-[10px] uppercase font-bold tracking-wider text-gold border border-gold/20">
                                ${p.tag}
                            </span>
                        </div>
                        <h3 class="font-syne text-xl font-bold mb-1">${p.name}</h3>
                        <p class="text-gray-400 text-xs leading-relaxed mb-4">${p.desc}</p>
                    </div>
                    <div class="flex items-center justify-between pt-4 border-t border-white/5">
                        <div>
                            <span class="text-[10px] text-gray-500 uppercase tracking-wider block">Price</span>
                            <span class="font-syne text-xl font-bold text-white">$${p.price}</span>
                        </div>
                        <button onclick="addToCart('${p.name}', ${p.price}, '${p.image}')" class="px-5 py-2.5 rounded-full bg-white/10 hover:bg-gold hover:text-dark text-white text-xs font-bold transition-all flex items-center gap-1.5">
                            <i data-lucide="shopping-bag" class="w-3.5 h-3.5"></i>
                            <span>Add to Bag</span>
                        </button>
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function addToCart(name, price, image) {
            const existing = cart.find(item => item.name === name);
            if (existing) {
                existing.qty += 1;
            } else {
                cart.push({ name, price, image, qty: 1 });
            }
            updateCartUI();
            showToast(`Added ${name} to your bag.`);
        }

        function updateCartUI() {
            const badge = document.getElementById('cart-badge');
            const list = document.getElementById('cart-items');
            const subtotalEl = document.getElementById('cart-subtotal');

            const totalCount = cart.reduce((acc, item) => acc + item.qty, 0);
            badge.innerText = totalCount;

            const total = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);
            subtotalEl.innerText = `$${total.toFixed(2)}`;

            if (cart.length === 0) {
                list.innerHTML = `<p class="text-gray-500 text-sm text-center py-8">Your bag is currently empty.</p>`;
            } else {
                list.innerHTML = cart.map((item, idx) => `
                    <div class="flex items-center gap-4 bg-white/5 p-3 rounded-2xl border border-white/5">
                        <img src="${item.image}" alt="${item.name}" class="w-14 h-14 object-cover rounded-xl">
                        <div class="flex-1 min-w-0">
                            <div class="font-syne text-sm font-bold truncate">${item.name}</div>
                            <div class="text-gray-400 text-xs">$${item.price} × ${item.qty}</div>
                        </div>
                        <button onclick="removeFromCart(${idx})" class="p-1.5 rounded-lg hover:bg-white/10 text-gray-400 hover:text-red-400">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                `).join('');
            }
            lucide.createIcons();
        }

        function removeFromCart(index) {
            cart.splice(index, 1);
            updateCartUI();
        }

        function toggleCart() {
            const drawer = document.getElementById('cart-drawer');
            const overlay = document.getElementById('cart-drawer-overlay');
            const isOpen = !drawer.classList.contains('translate-x-full');

            if (isOpen) {
                drawer.classList.add('translate-x-full');
                overlay.classList.add('opacity-0', 'pointer-events-none');
            } else {
                drawer.classList.remove('translate-x-full');
                overlay.classList.remove('opacity-0', 'pointer-events-none');
            }
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-msg').innerText = msg;
            toast.classList.remove('translate-y-20', 'opacity-0');
            setTimeout(() => {
                toast.classList.add('translate-y-20', 'opacity-0');
            }, 3000);
        }

        function checkout() {
            if (cart.length === 0) {
                showToast("Please add items to your bag first!");
                return;
            }
            alert("✨ Thank you for choosing MAISON NOIR! Your bespoke order has been processed.");
            cart = [];
            updateCartUI();
            toggleCart();
        }

        // Spotlight Mouse Hover Effect
        document.addEventListener('mousemove', (e) => {
            document.querySelectorAll('.card-spotlight').forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });

        // Initialize on load
        window.addEventListener('DOMContentLoaded', () => {
            renderProducts();
            lucide.createIcons();
        });
    </script>
</body>
</html>"""

target_path = os.path.join(os.path.splitdrive(os.getcwd())[0] + os.sep, "FRIDAY_Projects", "one_fully_functional_e", "index.html")
os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print("SUCCESSFULLY DEPLOYED TO:", target_path)
