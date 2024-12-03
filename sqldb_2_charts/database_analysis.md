# Sales Database Analysis

## Database Overview
- **Database File**: `sales_database.db`
- **Type**: SQLite
- **Size**: ~32KB

## Table Structure

### Sales Data Table (`sales_data`)

#### Schema
| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Postcode | INTEGER | Geographic postal code |
| Sales_Rep_ID | INTEGER | Unique identifier for sales representatives |
| Sales_Rep_Name | TEXT | Name of the sales representative |
| Year | INTEGER | Year of the sale |
| Value | REAL | Sales value (presumably in currency units) |

#### Indexes
The table has the following indexes for optimized querying:
- `idx_sales_rep` on `sales_rep_id`
- `idx_year` on `year`
- `idx_postcode` on `postcode`

#### Sample Data
```sql
Postcode | Sales_Rep_ID | Sales_Rep_Name | Year | Value
---------|--------------|----------------|------|-------
2121     | 456         | Jane           | 2011 | 84219.50
2092     | 789         | Ashish         | 2012 | 28322.19
2128     | 456         | Jane           | 2013 | 81878.99
2073     | 123         | John           | 2011 | 44491.14
2134     | 789         | Ashish         | 2012 | 71837.72
```

## Data Characteristics
- The database appears to track sales performance by representatives across different postcodes and years
- Sales representatives are identified by both ID and name
- Sales values are stored with high precision (floating-point numbers)
- The data spans multiple years
- Each record represents a sale value for a specific sales representative in a particular postcode and year

## Usage Notes
- The presence of indexes on postcode, sales_rep_id, and year suggests these are common filtering/grouping criteria

## Analysis Tasks

To perform the following analyses on `sales_database.db`:

### 1. Sales Performance by Geographic Region (Postcode)
```sql
-- Total sales by postcode
SELECT 
    Postcode,
    COUNT(*) as number_of_sales,
    ROUND(SUM(Value), 2) as total_sales,
    ROUND(AVG(Value), 2) as average_sale
FROM sales_data
GROUP BY Postcode
ORDER BY total_sales DESC;
```

#### Results
| Postcode | number_of_sales | total_sales | average_sale |
|----------|-----------------|-------------|--------------|
| 2049     | 3              | 274345.80   | 91448.60    |
| 2032     | 3              | 269275.09   | 89758.36    |
| 2193     | 3              | 242065.04   | 80688.35    |
| 2048     | 3              | 236497.98   | 78832.66    |
| 2164     | 3              | 234119.33   | 78039.78    |
| ...      | ...            | ...         | ...         |
| 2152     | 3              | 78186.25    | 26062.08    |
| 2117     | 3              | 62232.52    | 20744.17    |
| 2115     | 3              | 59202.23    | 19734.08    |
| 2170     | 3              | 48929.38    | 16309.79    |
| 2027     | 3              | 44248.59    | 14749.53    |
| 2007     | 3              | 30497.23    | 10165.74    |

Key Observations:
- Each postcode has exactly 3 sales records
- Highest performing postcode (2049) has total sales of $274,345.80 with an average of $91,448.60 per sale
- Lowest performing postcode (2007) has total sales of $30,497.23 with an average of $10,165.74 per sale
- There is significant variation in sales performance across postcodes, with a roughly 9x difference between highest and lowest performing areas

#### Visualization: Top 10 Postcodes by Total Sales

<div style="width: 800px; height: 400px;">
    <canvas id="postcodeSalesChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('postcodeSalesChart');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2049', '2032', '2193', '2048', '2164', '2031', '2166', '2128', '2125', '2150'],
            datasets: [{
                label: 'Total Sales ($)',
                data: [274345.80, 269275.09, 242065.04, 236497.98, 234119.33, 229417.51, 225959.50, 216232.35, 213338.83, 213236.54],
                backgroundColor: 'rgba(54, 162, 235, 0.8)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 10 Postcodes by Total Sales',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total Sales ($)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Postcode'
                    }
                }
            }
        }
    });
</script>

### 2. Individual Sales Representative Performance
```sql
-- Sales performance by representative
SELECT 
    Sales_Rep_ID,
    Sales_Rep_Name,
    COUNT(*) as number_of_sales,
    ROUND(SUM(Value), 2) as total_sales,
    ROUND(AVG(Value), 2) as average_sale
FROM sales_data
GROUP BY Sales_Rep_ID, Sales_Rep_Name
ORDER BY total_sales DESC;
```

### 3. Year-over-Year Trends
```sql
-- Annual sales trends
SELECT 
    Year,
    COUNT(*) as number_of_sales,
    ROUND(SUM(Value), 2) as total_sales,
    ROUND(AVG(Value), 2) as average_sale
FROM sales_data
GROUP BY Year
ORDER BY Year;
```

### 4. Regional Sales Patterns
```sql
-- Regional sales patterns by year
SELECT 
    Postcode,
    Year,
    COUNT(*) as number_of_sales,
    ROUND(SUM(Value), 2) as total_sales,
    ROUND(AVG(Value), 2) as average_sale
FROM sales_data
GROUP BY Postcode, Year
ORDER BY Postcode, Year;
