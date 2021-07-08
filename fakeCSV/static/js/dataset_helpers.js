window.onload = () => {
    const updateInterval = 5

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    axios.defaults.withCredentials = true;

    const appendNewRow = (response) => {
        const table_body = $('tbody');
        const last_row = table_body.children().last();
        const nums_row = last_row.find('th').html()

        table_body.append($(`<tr id="${response.data.task_id}" class="not_ready_dataset">
                    <th scope="row">${nums_row}</th>
                    <td>${new Date().toLocaleDateString("en-US", {year: 'numeric', month: 'long', day: 'numeric'})}</td>
                    <td>
                        <span class="badge btn-secondary">Processing</span>
                    </td>
                </tr>`));
    }

    const downloadDataset = (event) => {
        axios({
            method: 'get',
            url: `${window.location.hostname}/dataset/${event.target.id}/download`,
        }).then(response => {
            let link = document.createElement('a');
            document.body.appendChild(link);
            link.href = response.data.dataset_url;
            link.click();
            link.remove()
        })
    }


    const generateData = (e) => {
        const nums_input = $('#rows_amount');
        const generateButton = $('#generateData')
        generateButton.prop('disabled', true);
        axios({
            method: 'post',
            url: window.location.href,
            data: {
                rows_amount: nums_input.val()
            }
        }).then(response => {
            appendNewRow(response)
        }).catch(error => {
            console.error(error)
        }).finally(
            () => generateButton.prop('disabled', false)
        );
    }
    const updateDataSetStatus = (result_datasets) => {
        for (let dataset_id of result_datasets) {
            let row = $(`#${dataset_id}`)
            row.removeClass("not_ready_dataset")
            row.append($(`<td>
                        <button class="link" id="${dataset_id}">Download</button>
                    </td>`)[0])
            row.find('.link')[0].addEventListener('click', downloadDataset, true)
            let badge = row.find('.badge')
            badge.removeClass('btn-secondary')
            badge.addClass('btn-success')
            badge.html('Ready')

        }
    }

    const getTaskStatus = () => {
        let not_ready_rows = $('.not_ready_dataset')
        let task_list = []
        for (let row of not_ready_rows) {
            task_list.push(row.id)
        }
        if (task_list.length > 0) {
            axios({
                method: 'post',
                url: `/dataset/results`,
                data: {
                    task_list
                }
            }).then(response => {
                updateDataSetStatus(response.data.result_datasets)
            }).catch(error => {
                console.error(error)
            })
        }
    }

    $('#generateDataForm').submit(function (e) {
        e.preventDefault();
        generateData(e)
    });

    setInterval(getTaskStatus, updateInterval * 1000);
}

