document.addEventListener('alpine:init', () => {
    Alpine.store('func', {
        frag(url, ref) {
            fetch(url).catch(error => {
                console.log(error);
            }).then((response) => {
                if (response.status === 200) {
                    response.text().then((text) => {
                        ref.innerHTML = text;
                    });
                }
            })
        }
    });
});