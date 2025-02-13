/**
 * 
 * @param {string} endpoint - path to server request
 * @param {Map} request - request to send it to server
 * @returns promise to server answer data or error
 */
export const sendAsync = async (endpoint, request) => {
    const response = await fetch(endpoint, request);

    if (!response.ok) {
        return response.json().then(err => { throw err; }).catch(err => { throw err; });
    }
    if (response.statusText === "No Content") return response.text();
    return response.json();
};