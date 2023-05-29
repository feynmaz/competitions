class Main {
    constructor() {
        this.tableWrapper = document.querySelector('.table-wrapper');
        this.importForm = document.querySelector('.import-form');
        this.reportForm = document.querySelector('.report-form');

        this.dateRangePickerElement = document.querySelector('.datetime');

        this.createInstances();
        this.hangEvents();
    }

    createInstances() {
        this.dateRangePicker = new DateRangePicker(this.dateRangePickerElement, {
            format: 'dd.mm.yyyy'
        })
    }

    hangEvents() {
        this.importForm.addEventListener('submit', (event) => this.handleSubmitImportForm(event));
        this.reportForm.addEventListener('submit', (event) => this.handleSubmitReportForm(event));
    }

    handleSubmitImportForm(event) {
        event.preventDefault();
        const formData = new FormData(this.importForm);
        this.importFile(formData);
    }

    handleSubmitReportForm(event) {
        event.preventDefault();
        const formData = new FormData(this.reportForm);
        const params = {};
        Array.from(formData.entries()).forEach(field => {
            params[field[0]] = field[1]
        })
        this.getReport(params);
    }

    importFile(formData) {
        const options = {
            method: 'POST',
            body: formData,
        };
        fetch('/', options)
            .then((response) => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const data = doc.querySelector('.table-wrapper');
                this.tableWrapper.innerHTML = data.innerHTML;
                alert("Файл успешно загружен")
            })
            .catch(() => alert("Ошибка импорта"))
    }

    getReport(params) {
        let url = "/report";
        const options = {
            method: 'GET'
        };

        url += '?' + new URLSearchParams(params);

        fetch(url, options)
            .then(response => response.text())
            .then(data => this.tableWrapper.innerHTML = data)
            .catch(error => console.error(error))
    }
}

new Main();

