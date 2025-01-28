import { fetchDataFromTable } from './api/supabase.js';

// Fetch data for charts
// Separate data fetching
async function fetchData() {
    try {
        const data1 = await fetchDataFromTable('defense_top10_value_pct_gdp_2023');
        const data2 = await fetchDataFromTable('defense_top10_value_usd_per_capita_2023');
        const data3 = await fetchDataFromTable('defense_top10_value_ppp_2023');
        // ... fetch more datasets as needed
        
        // After fetching all data, render the charts
        renderChart(data1, 'chart1', 'First Chart', '%');
        renderChart(data2, 'chart2', 'Second Chart', '$');
        renderChart(data3, 'chart3', 'Third Chart', '$');
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


function renderChart(data, containerId, title = '', unit = '') {

    if (data.length === 0) {
        console.error('No data available for charting.');
        return;
    }

    // Process data (example: extract x and y values)
    let chartData = data.map(item => ({
        x: item.value,
        y: item.countryname
    }));

    // Sort data by x values in ascending order
    chartData.sort((a, b) => a.x - b.x);

    // Extract sorted x and y values
    const xValues = chartData.map(item => item.x);
    const yValues = chartData.map(item => item.y);
    const textValues = xValues.map(value => unit === '%' ? `${(value * 100).toFixed(1)}%` : `$${value.toFixed(2)}`);

    // Determine tickformat based on unit
    const tickformat = unit === '%' ? ',.2%' : '$,.2f';

    // Plotly chart
    const plotlyData = [
        {
            x: xValues,
            y: yValues,
            type: 'bar',
            orientation: 'h',
            text: textValues,
            textposition: 'auto'
        }
    ];

    const layout = {
        title: title,
        xaxis: { 
            //title: 'Percentage of GDP',
            tickformat: tickformat, // Format x-axis values as percentages
            showticklabels: false
        },
        yaxis: {
            automargin: true
        }
    };

    Plotly.newPlot(containerId, plotlyData, layout);
}

// Initialize everything
//fetchData();
// Call the render function once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', fetchData);