import { fetchDataFromTable } from './api/supabase.js';

async function renderCharts() {
    // Fetch data from Supabase
    const data = await fetchDataFromTable('defense_top10_value_pct_gdp_2023');

    if (data.length === 0) {
        console.error('No data available for charting.');
        return;
    }

    // Process data (example: extract x and y values)
    const xValues = data.map(item => item.value_pct_gdp);
    const yValues = data.map(item => item.countryname);
    const textValues = xValues.map(value => `${(value * 100).toFixed(1)}%`);

    // Plotly chart
    const chartData = [
        {
            x: xValues,
            y: yValues,
            type: 'bar',
            orientation: 'h',
            text: textValues
        }
    ];

    const layout = {
        title: 'Supabase Data Chart',
        xaxis: { 
            title: 'Percentage of GDP',
            tickformat: ',.1%'
        },
        //yaxis: { title: 'Y-Axis Label' }
    };

    Plotly.newPlot('chartDiv', chartData, layout);
}

// Call the render function once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', renderCharts);
