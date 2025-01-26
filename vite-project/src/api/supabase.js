import { createClient } from '@supabase/supabase-js';

// Access the Supabase credentials from process.env
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_KEY;

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