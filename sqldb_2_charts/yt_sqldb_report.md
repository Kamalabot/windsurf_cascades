# Sales Database Analysis Report

## Database Structure
The database contains a single table named `sales_data` with the following schema:

```sql
CREATE TABLE IF NOT EXISTS "sales_data" (
  "Postcode" INTEGER,
  "Sales_Rep_ID" INTEGER,
  "Sales_Rep_Name" TEXT,
  "Year" INTEGER,
  "Value" REAL
);
```

## Sales Analysis Queries and Results

### 1. Total Sales by Year
```sql
SELECT Year, ROUND(SUM(Value), 2) as Total_Sales
FROM sales_data
GROUP BY Year
ORDER BY Year;
```

Results:
| Year | Total_Sales |
|------|-------------|
| 2011 | 6576385.89  |
| 2012 | 6151939.97  |
| 2013 | 6471135.57  |

### 2. Top 5 Sales Representatives by Total Sales
```sql
SELECT Sales_Rep_Name, 
       ROUND(SUM(Value), 2) as Total_Sales,
       COUNT(*) as Number_of_Sales
FROM sales_data
GROUP BY Sales_Rep_Name
ORDER BY Total_Sales DESC
LIMIT 5;
```

Results:
| Sales_Rep_Name | Total_Sales | Number_of_Sales |
|----------------|-------------|-----------------|
| Jane           | 6665269.38  | 130             |
| Ashish         | 6386039.23  | 130             |
| John           | 6148152.83  | 130             |

### 3. Sales Analysis by Postcode
```sql
SELECT 
    Postcode,
    ROUND(SUM(Value), 2) as Total_Sales,
    ROUND(AVG(Value), 2) as Avg_Sale_Value,
    COUNT(*) as Number_of_Sales
FROM sales_data
GROUP BY Postcode
ORDER BY Total_Sales DESC
LIMIT 5;
```

Results:
| Postcode | Total_Sales | Avg_Sale_Value | Number_of_Sales |
|----------|-------------|----------------|-----------------|
| 2049     | 274345.8    | 91448.6        | 3               |
| 2032     | 269275.09   | 89758.36       | 3               |
| 2193     | 242065.04   | 80688.35       | 3               |
| 2048     | 236497.98   | 78832.66       | 3               |
| 2164     | 234119.33   | 78039.78       | 3               |

### Visual Representation of Sales by Postcode

<div style="width: 800px; margin: 20px auto;">
    <canvas id="salesByPostcodeChart"></canvas>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('salesByPostcodeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2049', '2032', '2193', '2048', '2164'],
            datasets: [{
                label: 'Total Sales ($)',
                data: [274345.8, 269275.09, 242065.04, 236497.98, 234119.33],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)',
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(255, 99, 132, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Top 5 Postcodes by Total Sales',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Total Sales ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Postcode'
                    }
                }
            }
        }
    });
});
</script>

## Summary of Findings

1. **Yearly Sales Performance**:
   - Highest sales were in 2011 ($6.58M)
   - Slight dip in 2012 ($6.15M)
   - Recovery in 2013 ($6.47M)

2. **Sales Representatives Performance**:
   - Jane is the top performer with $6.67M in total sales
   - Ashish follows with $6.39M
   - John rounds out the top 3 with $6.15M
   - All representatives have the same number of sales (130)

3. **Geographic Analysis**:
   - Postcode 2049 shows the highest total sales ($274,346)
   - Top 5 postcodes all show similar patterns with 3 sales each
   - Average sale values in top postcodes range from $78,040 to $91,449
