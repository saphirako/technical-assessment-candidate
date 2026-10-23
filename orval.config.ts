import { defineConfig } from 'orval';

export default defineConfig({
    api: {
        input: {
            target: 'http://localhost:8000/swagger',
        },
        output: {
            target: 'frontend/app/services/api/generated',
            schemas: 'frontend/app/services/api/generated/model',
            client: 'fetch',
            mode: 'tags-split',
            clean: true,
            indexFiles: true,
            baseUrl: {
                runtime: 'API_BASE_URL',
                imports: [{ name: 'API_BASE_URL', importPath: 'app/services/api/baseApi' }],
            },
        },
    },
});
