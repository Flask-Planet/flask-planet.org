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
        },
        strip_form(list_of_refs) {
            let temp_dict = {}
            for (let ref of list_of_refs) {
                if (ref !== undefined) {
                    for (let element of ref.elements) {
                        if (
                            element.type === 'hidden'
                            || element.type === 'text'
                            || element.type === 'number'
                            || element.type === 'email'
                            || element.type === 'date'
                        ) {
                            temp_dict[element.name] = element.value
                        }
                    }
                }
            }
            return temp_dict
        },
    });
});