let page = 1;
let loading = false;
const container = document.getElementById('product-container');
const loadingElement = document.getElementById('loading');

// Infinite Scroll Logic
window.addEventListener('scroll', function() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !loading) {
        loadMoreProducts();
    }
});

// Function to Load More Products
function loadMoreProducts() {
    page++;
    loading = true;
    loadingElement.style.display = 'block';

    // Fetch the next page of products
    fetch(`?page=${page}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Append new products to the container
        data.products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';
            productCard.innerHTML = `
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>${product.description}</p>
                <p>Price: $${product.price}</p>
                <p>Store: ${product.store}</p>
                <p>Category: ${product.category}</p>
            `;
            container.appendChild(productCard);
        });

        // Hide loading indicator
        loading = false;
        loadingElement.style.display = 'none';

        // Stop loading if there are no more products
        if (!data.has_next) {
            window.removeEventListener('scroll');
        }
    });
}