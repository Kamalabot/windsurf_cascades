# E-Commerce Product Performance Dashboard

## Rendering Note
> **Important**: This dashboard supports multiple rendering methods:
> - Interactive Chart.js (local/supported environments)
> - Static QuickChart images (GitHub/universal compatibility)

## Product Performance Overview (Interactive Chart.js)

<div style="width: 100%; display: flex; flex-wrap: wrap; justify-content: space-between;">
    <div style="width: 48%;">
        <canvas id="salesChart"></canvas>
    </div>
    <div style="width: 48%;">
        <canvas id="reviewChart"></canvas>
    </div>
    <div style="width: 48%; margin-top: 20px;">
        <canvas id="quantityChart"></canvas>
    </div>
    <div style="width: 48%; margin-top: 20px;">
        <canvas id="priceChart"></canvas>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// E-commerce Product Data
const productData = {
    products: [
        { name: 'Wireless Headphones', price: 129.99, sales: 1250, quantity: 500, reviews: 4.5 },
        { name: 'Smart Watch', price: 199.99, sales: 950, quantity: 300, reviews: 4.7 },
        { name: 'Bluetooth Speaker', price: 79.99, sales: 1500, quantity: 750, reviews: 4.3 },
        { name: 'Fitness Tracker', price: 89.99, sales: 800, quantity: 400, reviews: 4.6 },
        { name: 'Noise Cancelling Earbuds', price: 159.99, sales: 650, quantity: 250, reviews: 4.8 }
    ]
};

// Sales Chart
new Chart(document.getElementById('salesChart'), {
    type: 'bar',
    data: {
        labels: productData.products.map(p => p.name),
        datasets: [{
            label: 'Total Sales',
            data: productData.products.map(p => p.sales),
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'Product Sales Performance' }
        }
    }
});

// Reviews Chart
new Chart(document.getElementById('reviewChart'), {
    type: 'radar',
    data: {
        labels: productData.products.map(p => p.name),
        datasets: [{
            label: 'Customer Reviews',
            data: productData.products.map(p => p.reviews),
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            pointBackgroundColor: 'rgba(255, 99, 132, 1)'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'Product Ratings' }
        }
    }
});

// Quantity Chart
new Chart(document.getElementById('quantityChart'), {
    type: 'pie',
    data: {
        labels: productData.products.map(p => p.name),
        datasets: [{
            data: productData.products.map(p => p.quantity),
            backgroundColor: [
                'rgba(255, 206, 86, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 99, 132, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)'
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'Inventory Quantity' }
        }
    }
});

// Price Chart
new Chart(document.getElementById('priceChart'), {
    type: 'line',
    data: {
        labels: productData.products.map(p => p.name),
        datasets: [{
            label: 'Product Prices',
            data: productData.products.map(p => p.price),
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: { display: true, text: 'Product Pricing' }
        }
    }
});
</script>

## Product Performance Overview (Static Images)

### Sales Performance
![Sales Chart](https://quickchart.io/chart?c=%7Btype%3A%27bar%27%2Cdata%3A%7Blabels%3A%5B%27Wireless%20Headphones%27%2C%27Smart%20Watch%27%2C%27Bluetooth%20Speaker%27%2C%27Fitness%20Tracker%27%2C%27Noise%20Cancelling%20Earbuds%27%5D%2Cdatasets%3A%5B%7Blabel%3A%27Total%20Sales%27%2Cdata%3A%5B1250%2C950%2C1500%2C800%2C650%5D%7D%5D%7D%7D)

### Product Ratings
![Reviews Chart](https://quickchart.io/chart?c=%7Btype%3A%27radar%27%2Cdata%3A%7Blabels%3A%5B%27Wireless%20Headphones%27%2C%27Smart%20Watch%27%2C%27Bluetooth%20Speaker%27%2C%27Fitness%20Tracker%27%2C%27Noise%20Cancelling%20Earbuds%27%5D%2Cdatasets%3A%5B%7Blabel%3A%27Customer%20Reviews%27%2Cdata%3A%5B4.5%2C4.7%2C4.3%2C4.6%2C4.8%5D%7D%5D%7D%7D)

### Inventory Quantity
![Quantity Chart](https://quickchart.io/chart?c=%7Btype%3A%27pie%27%2Cdata%3A%7Blabels%3A%5B%27Wireless%20Headphones%27%2C%27Smart%20Watch%27%2C%27Bluetooth%20Speaker%27%2C%27Fitness%20Tracker%27%2C%27Noise%20Cancelling%20Earbuds%27%5D%2Cdatasets%3A%5B%7Bdata%3A%5B500%2C300%2C750%2C400%2C250%5D%7D%5D%7D%7D)

### Product Pricing
![Price Chart](https://quickchart.io/chart?c=%7Btype%3A%27line%27%2Cdata%3A%7Blabels%3A%5B%27Wireless%20Headphones%27%2C%27Smart%20Watch%27%2C%27Bluetooth%20Speaker%27%2C%27Fitness%20Tracker%27%2C%27Noise%20Cancelling%20Earbuds%27%5D%2Cdatasets%3A%5B%7Blabel%3A%27Product%20Prices%27%2Cdata%3A%5B129.99%2C199.99%2C79.99%2C89.99%2C159.99%5D%7D%5D%7D%7D)

## Product Details

| Product Name | Price | Total Sales | Inventory | Average Review |
|-------------|-------|-------------|-----------|----------------|
| Wireless Headphones | $129.99 | 1,250 | 500 | 4.5/5 |
| Smart Watch | $199.99 | 950 | 300 | 4.7/5 |
| Bluetooth Speaker | $79.99 | 1,500 | 750 | 4.3/5 |
| Fitness Tracker | $89.99 | 800 | 400 | 4.6/5 |
| Noise Cancelling Earbuds | $159.99 | 650 | 250 | 4.8/5 |

## Key Insights

1. **Best Selling Product**: Bluetooth Speaker (1,500 sales)
2. **Highest Rated Product**: Noise Cancelling Earbuds (4.8/5)
3. **Highest Priced Product**: Smart Watch ($199.99)
4. **Largest Inventory**: Bluetooth Speaker (750 units)

## Performance Metrics

- **Total Revenue**: $5,149.45
- **Average Product Rating**: 4.58/5
- **Total Units Sold**: 4,150
- **Total Inventory**: 2,200 units

## Rendering Methods

### 1. Interactive Dashboard
- Requires local environment with Chart.js support
- Full interactivity and dynamic rendering
- Best for detailed exploration

### 2. Static Image Charts
- Universal compatibility
- Renders on GitHub and static markdown viewers
- Quick visual overview

## Technical Notes

- Interactive charts powered by Chart.js
- Static images generated via QuickChart.io
- Consistent data representation across methods
