import { fetchDataFromTable } from './api/supabase.js';
import './styles.scss';

// Fetch data for charts
// Separate data fetching
async function fetchData() {
    try {
        const data1 = await fetchDataFromTable('defense_top10_value_pct_gdp_2023');
        const data2 = await fetchDataFromTable('defense_top10_value_usd_per_capita_2023');
        const data3 = await fetchDataFromTable('defense_top10_value_ppp_2023');
        // ... fetch more datasets as needed
        
        // After fetching all data, render the charts
        renderChart(data1, 'chart1', '% of GDP', ',.1%');
        renderChart(data2, 'chart2', 'USD per Capita', '$,.0f');
        renderChart(data3, 'chart3', 'Total Spend (PPP)', '$,.1T');
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}


function renderChart(data, containerId, title = '', tickformat = '') {

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
    const textValues = xValues.map(value => {
        if (tickformat.includes('%')) {
            return value !== undefined ? `${(value * 100).toFixed(1)}%` : 'N/A';
        } else if (tickformat.includes('T')) {
            return value !== undefined ? `$${(value / 1e9).toFixed(1)}B` : 'N/A';
        } else {
            return value !== undefined ? `$${Math.round(value).toLocaleString()}` : 'N/A';
        }
    });

    // Plotly chart
    const plotlyData = [
        {
            x: xValues,
            y: yValues,
            type: 'bar',
            orientation: 'h',
            text: textValues,
            textposition: 'auto',
            marker: {
                color: '#C4F1BE'
            }
        }
    ];

    const layout = {
        title: title,
        font: {
            color: '#FFFFFF'
        },
        xaxis: { 
            //title: 'Percentage of GDP',
            tickformat: tickformat, // Format x-axis values as percentages
            showticklabels: false,
            showgrid: false
        },
        yaxis: {
            automargin: true,
            showgrid: false
        },
        autosize: true,
        height: 400,
        margin: {
            l: 20,
            r: 10,
            t: 50,
            b: 40
        },
        plot_bgcolor: '#525B76',
        paper_bgcolor: '#525B76'
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot(containerId, plotlyData, layout, config);
}

// Initialize everything
// Call the render function once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', fetchData);