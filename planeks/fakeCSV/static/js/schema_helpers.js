$(document).ready(() => {
    console.log("loaded script")
    const removeColumn = (event) => {
        event.preventDefault()
        let column = $(event.target).parent('.schema_column')
        column.remove()
    }

    const buttons = $('.deleteColumn')
    for (const button of buttons) {
        button.addEventListener('click', removeColumn, true)
    }
})