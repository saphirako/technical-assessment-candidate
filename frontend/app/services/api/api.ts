import { api } from './baseApi';
import { fromOrval } from './orval-query';
import { postApiReplacements } from './generated/replacements/replacements';
import type { ReplacementRequest } from './generated/model';

export const replacementsApi = api.injectEndpoints({
    endpoints: (builder) => ({
        findReplacements: builder.mutation({
            queryFn: (body: ReplacementRequest) => fromOrval(() => postApiReplacements(body)),
        }),
    }),
});

export const { useFindReplacementsMutation } = replacementsApi;
