window.onload = () => {
    let counter = 1

    const removeColumn = (event) => {
        event.preventDefault()
        let column = $(event.target).parent().parent('.schema_column')
        column.remove()
    }

    const addNewColumn = (event) => {
        event.preventDefault()

        let column = $($(event.target).parent().find('.new-append-column')[0])

        let newColumn = column.clone()
        newColumn.removeClass('new-append-column').addClass('schema_column')

        newColumn.find('[name^=column]').each(function (i) {
            $(this).attr('name', $(this).attr('name') + '.new' + counter);
        });

        let clearButton = newColumn.find('.btn')
        let clearButtonParent = clearButton.parent()
        clearButton.remove()

        let button = $(`<div class="flex-row-reverse">
                            <button class="btn btn-danger deleteColumn">Delete</button>
                        </div>`)[0]

        clearButtonParent.append(button)
        newColumn.find('.btn')[0].addEventListener('click', removeColumn, true)

        let type_select = newColumn.find('[name^=column_type]')
        type_select[0].addEventListener('change', handleType, true)

        type_select.val(column.find('[name^=column_type]').val()).change()

        let referenceNode = $('#columns')
        referenceNode.after(newColumn)

        counter += 1
        clearColumn(event)
    }

    const clearNonRequired = (event) => {
        let event_target = $(event.target)

        if (event_target.hasClass('form-select')) {
            event_target = event_target[0].parentElement.parentElement
        } else {
            event_target = event_target[0].parentElement
        }

        let non_required_inputs = $(event_target).find('.non_required')
        for (let non_required of non_required_inputs) {
            non_required.remove()
        }
        return event.target.parentElement
    }

    const handleType = (event) => {
        let event_target = clearNonRequired(event)
        console.log(event_target)
        if (event.target.value === 'INTEGER') {
            event_target.after($(`<div class="non_required col"><label for="id_column_from" class="col-form-label">Column from:</label>
                <input type="number" id="id_column_from" name="column_from" class="form-control"></div>`)[0])
            event_target.after($(`<div class="non_required col"><label for="id_column_to" class="col-form-label">Column to:</label>
                <input type="number" id="id_column_to" name="column_to" class="form-control"></div>`)[0])
        } else if (event.target.value === 'TEXT') {
            event_target.after($(
                `<div class="non_required col"><label for="id_column_to" class="col-form-label">Amount of sentences:</label>
                <input type="number" id="id_column_to" name="column_to" class="form-control"></div>`)[0]
            )
        }
    }

    const clearColumn = (event) => {
        event.preventDefault()
        let newColumn = $(event.target).parent()
        if ($(event.target).id === 'clear-button') {
            newColumn = newColumn.parent()
        }
        newColumn.find('[name^=column]').val('')
        newColumn.find('#id_column_type_new').val('EMAIL').change()
        clearNonRequired(event)
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

