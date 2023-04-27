document.addEventListener('alpine:init', () => {
    Alpine.store('alpine:resources:add', {
        value: '# Write Some Markdown...',
        init() {
            let editor = new SimpleMDE({element: this.$refs.editor})

            editor.value(this.value)

            editor.codemirror.on('change', () => {
                this.value = editor.value()
            })
        },
    });
});