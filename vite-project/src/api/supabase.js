//import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

// Access the Supabase credentials from process.env
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_KEY = process.env.SUPABASE_KEY;

// Initialize Supabase client
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export async function fetchDataFromTable(tableName) {
    try {
        const { data, error } = await supabase
            .from(tableName)
            .select('*');
        if (error) throw error;
        return data;
    } catch (error) {
        console.error('Error fetching data:', error.message);
        return [];
    }
}

// Call the function to fetch and log data
//(async () => {
//    const result = await fetchDataFromTable('defense_top10_value_pct_gdp_2023');
//    console.log(result);
//})();