document.addEventListener('alpine:init', () => {
    Alpine.store('simple_mde', {
        load_simple_mde(element) {
            let editor = new SimpleMDE({element: element})

            editor.value(element.value)

            editor.codemirror.on('change', () => {
                element.value = editor.value()
            })
        },
    });
})
