window.onload = () => {
    let counter = 1

    const removeColumn = (event) => {
        event.preventDefault()
        let column = $(event.target).parent('.schema_column')
        column.remove()
    }

    const addNewColumn = (event) => {
        event.preventDefault()

        let column = $($(event.target).parent()[0])

        let newColumn = column.clone()
        newColumn.removeClass('new-append-column').addClass('schema_column')

        newColumn.find('[name^=column]').each(function (i) {
            $(this).attr('name', $(this).attr('name') + '.new' + counter);
        });

        newColumn.find('.btn').remove()

        let button = $('<button class="btn btn-danger deleteColumn">Delete</button>')[0]
        newColumn.append(button)
        newColumn.find('.btn')[0].addEventListener('click', removeColumn, true)

        let type_select = newColumn.find('[name^=column_type]')
        type_select[0].addEventListener('change', handleType, true)

        type_select.val(column.find('[name^=column_type]').val()).change()

        $('#columns').next().append(newColumn)

        counter += 1
        clearNonRequired(event)
        clearColumn(event)
    }

    const clearNonRequired = (event) => {
        let event_target = $(event.target.parentElement)
        event_target.find('.non_required').remove()
        return event_target
    }

    const handleType = (event) => {
        let event_target = clearNonRequired(event)

        if (event.target.value === 'INTEGER') {
            event_target.append($(`<div class="non_required"><label for="id_column_from">Column from:</label>
                <input type="number" id="id_column_from" name="column_from"></div>`))
            event_target.append($(`<div class="non_required"><label for="id_column_to">Column to:</label>
                <input type="number" id="id_column_to" name="column_to"></div>`))
        } else if (event.target.value === 'TEXT') {
            event_target.append($(
                `<div class="non_required"><label for="id_column_to">Amount of sentences:</label>
                <input type="number" id="id_column_to" name="column_to"></div>`)
            )
        }
    }

    const clearColumn = (event) => {
        event.preventDefault()
        let newColumn = $(event.target).parent()
        newColumn.find('[name^=column]').val('')
        newColumn.find('#id_column_type_new').val('EMAIL').change()
    }

    const buttons = $('.deleteColumn')
    for (const button of buttons) {
        button.addEventListener('click', removeColumn, true)
    }

    $('#append-button')[0].addEventListener('click', addNewColumn, true)
    $('#clear-button')[0].addEventListener('click', clearColumn, true)

    const selects = $('[name^=column_type]')
    for (const select of selects) {
        select.addEventListener('change', handleType, true)
    }


}

