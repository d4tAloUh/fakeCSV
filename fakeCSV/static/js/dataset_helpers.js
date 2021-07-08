window.onload = () => {
    const updateInterval = 5

    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = 'X-CSRFToken'
    axios.defaults.withCredentials = true;

    taskList = []

    const appendNewRow = (response) => {
        const table_body = $('tbody');
		const last_row = table_body.children().last();
		const trc = $($('script[data-template="appendTableRow"]').html().trim()).clone();
		const nums_row = last_row.find('th').html()
        console.log(nums_row)

		trc.attr('task_id', task_id);
		trc.children('#index').text((nums_row ? +nums_row : 0) + 1);
		trc.find('#date_created').text((new Date()).toISOString().split('T') [0]);
		trc.find('#status').text('Processing');

		tb.append(trc);
        console.log(response)
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

