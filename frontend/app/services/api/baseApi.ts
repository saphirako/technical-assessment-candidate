import { createApi } from '@reduxjs/toolkit/query/react';
import { fetchBaseQuery } from '@reduxjs/toolkit/query';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const baseQuery = fetchBaseQuery({
    baseUrl: API_BASE_URL,
});

export const api = createApi({
    reducerPath: 'api',
    baseQuery,
    tagTypes: [],
    endpoints: () => ({}),
});

