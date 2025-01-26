console.log('script loaded');

import { fetchDataFromTable } from './api/supabase.js';

async function renderCharts() {
    // Fetch data from Supabase
    const data = await fetchDataFromTable('defense_top10_value_pct_gdp_2023');
    console.log('this is a test');

    if (data.length === 0) {
        console.error('No data available for charting.');
        return;
    }

    // Process data (example: extract x and y values)
    const xValues = data.map(item => item.countryname); // Replace with your column names
    const yValues = data.map(item => item.value_pct_gdp);

    // Plotly chart
    const chartData = [
        {
            x: xValues,
            y: yValues,
            type: 'bar'
        }
    ];

    const layout = {
        title: 'Supabase Data Chart',
        xaxis: { title: 'X-Axis Label' },
        yaxis: { title: 'Y-Axis Label' }
    };

    Plotly.newPlot('chartDiv', chartData, layout);
}

// Call the render function once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', renderCharts);
