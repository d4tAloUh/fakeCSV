$(document).ready(() => {
    const removeColumn = (event) => {
        let column = $(event.target).parent('.schema_column')
        console.log(column)
    }
    $('#deleteColumn').onclick = removeColumn
})