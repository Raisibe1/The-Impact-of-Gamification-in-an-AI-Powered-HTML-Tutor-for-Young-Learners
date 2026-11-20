export class APIError extends Error {
    constructor(message, status) {
        super(message);
        this.name = 'APIError';
        this.status = status;
    }
}

export class AuthError extends APIError {
    constructor(message = 'Not authenticated') {
        super(message, 401);
        this.name = 'AuthError';
    }
}

export class QuestAPI {
    constructor(base = '') {
        this.base = base;
    }

    
async _request(method, path, body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
    };

    if (body !== null) {
        options.body = JSON.stringify(body);
    }

    let res;

    try {
        res = await fetch(this.base + path, options);
    } catch (err) {
        console.error('Network request failed:', {
            method,
            path,
            message: err.message,
        });
        throw err;
    }

    const responseText = await res.text();

    let data = {};
    try {
        data = responseText ? JSON.parse(responseText) : {};
    } catch {
        data = { raw_response: responseText };
    }

    if (res.status === 401) {
        throw new AuthError(
            data.detail || 'Not authenticated'
        );
    }

    if (!res.ok) {
        console.error('Quest API request failed:', {
            method,
            url: this.base + path,
            status: res.status,
            response: data,
            requestBody: body,
        });

        throw new APIError(
            data.detail || data.raw_response || res.statusText,
            res.status
        );
    }

    return data;
}


    // ---- endpoints ----
    getState() {
        return this._request('GET', '/api/state');
    }

    awardXP({ amount, reason, lessonSlug = null, challengeSlug = null }) {
        return this._request('POST', '/api/xp', {
            amount,
            reason,
            lesson_slug: lessonSlug,
            challenge_slug: challengeSlug,
        });
    }

    saveProgress({ lessonSlug, challengeSlug = null, completed = true,
                   score = null, responseData = null }) {
        return this._request('POST', '/api/progress', {
            lesson_slug: lessonSlug,
            challenge_slug: challengeSlug,
            completed,
            score,
            response_data: responseData,
        });
    }

    unlockBadge(slug) {
        return this._request('POST', '/api/badges/unlock', { slug });
    }

    reset() {
        return this._request('POST', '/api/reset');
    }
}