function copyCookieValueToClipboard(cookieName) {
    const cookieValue = document.cookie
        .split('; ')
        .find(cookie => cookie.startsWith(cookieName + '='));

    if (cookieValue) {
        const value = cookieValue.split('=')[1];
        const textArea = document.createElement('textarea');
        textArea.value = value;
        document.body.appendChild(textArea);
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            const msg = successful ? 'Text copied to clipboard successfully.' : 'Unable to copy text to clipboard.';
            console.log(msg);
        } catch (err) {
            console.error('Unable to copy text to clipboard: ', err);
        } finally {
            document.body.removeChild(textArea);
        }
    } else {
        console.error('Cookie not found.');
    }
}

copyCookieValueToClipboard('yourCookieName');
