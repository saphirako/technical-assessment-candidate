import type { FetchBaseQueryError, QueryReturnValue } from '@reduxjs/toolkit/query';

type Status2xx = 200 | 201 | 202 | 203 | 204 | 205 | 206 | 207 | 208 | 226;

type SuccessArm<T> = { status: Status2xx; data: T; headers: Headers };

type ErrorArm = { status: number; data: unknown; headers: Headers };

function is2xx<T>(response: SuccessArm<T> | ErrorArm): response is SuccessArm<T> {
    return response.status >= 200 && response.status < 300;
}

function toFetchError(cause: unknown): FetchBaseQueryError {
    return {
        status: 'FETCH_ERROR',
        error: cause instanceof Error ? cause.message : String(cause),
    };
}

export async function fromOrval<T>(
    call: () => Promise<SuccessArm<T> | ErrorArm>,
): Promise<QueryReturnValue<T, FetchBaseQueryError, undefined>> {
    const [settled] = await Promise.allSettled([call()]);
    if (settled.status === 'rejected') {
        return { error: toFetchError(settled.reason) };
    }
    const response = settled.value;
    return is2xx(response)
        ? { data: response.data }
        : { error: { status: response.status, data: response.data } };
}
