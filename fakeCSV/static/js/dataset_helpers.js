window.onload = () => {
    const updateInterval = 5

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    axios.defaults.withCredentials = true;

    taskList = []

    const appendNewRow = (response) => {
        const table_body = $('tbody');
		const last_row = table_body.children().last();
		const nums_row = last_row.find('th').html()

		table_body.append($(`<tr id="${response.data.task_id}">
                    <th scope="row">${nums_row}</th>
                    <td>${new Date().toLocaleDateString("en-US",{ year: 'numeric', month: 'long', day: 'numeric' })}</td>
                    <td>
                        <span class="badge btn-secondary">Processing</span>
                    </td>
                </tr>`));
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
    const getTaskStatus = () => {

    }

    $('#generateDataForm').submit(function (e) {
        e.preventDefault();
        generateData(e)
    });

    setInterval(getTaskStatus, updateInterval * 1000);
}

