class Main {
    constructor() {
        this.contentWrapper = document.querySelector(".content-wrapper");
        this.importForm = document.querySelector(".import-form");
        this.reportForm = document.querySelector(".filter-form");

        this.dateFromInput = document.querySelector(".filter__date-from");
        this.dateToInput = document.querySelector(".filter__date-to");
        this.levelSelect = document.querySelector(".filter__level");
        this.positionSelect = document.querySelector(".filter__position");
        this.filterButton = document.querySelector(".filter__button");
        this.cleanButton = document.querySelector(".clean-button");

        this.dateRangePickerElement = document.querySelector('.datetime');

        this.createInstances();
        this.hangEvents();
    }

    createInstances() {
        this.dateRangePicker = new DateRangePicker(this.dateRangePickerElement, {
            format: "dd.mm.yyyy"
        });
        NiceSelect.bind(this.levelSelect, {searchable: true});
        NiceSelect.bind(this.positionSelect, {searchable: true});
    }

    hangEvents() {
        this.importForm.addEventListener("submit", (event) => this.handleSubmitImportForm(event));
        this.reportForm.addEventListener("submit", (event) => this.handleSubmitReportForm(event));
        this.cleanButton.addEventListener("click", () => this.cleanDb());
    }

    handleSubmitImportForm(event) {
        event.preventDefault();
        const formData = new FormData(this.importForm);
        this.importFile(formData);
    }

    handleSubmitReportForm(event) {
        event.preventDefault();
        const params = new URLSearchParams();
        const formData = new FormData(this.reportForm);
        Array.from(formData.entries()).forEach(field => {
            params.append(field[0], field[1]);
        })
        this.getReport(params.toString());
    }

    importFile(formData) {
        this.makeRequest({
            url: "/",
            options: { 
                method: "POST",
                body: formData,
            },
            onSuccess: () => alert("Файл успешно импортирован"),
            onError: () => alert("Ошибка импорта")
        })
    }

    getReport(params) {
        this.makeRequest({
            url: "/report?" + params,
            options: { 
                method: "GET"
            },
            onError: () => alert("Ошибка применения фильтра. Попробуйте позже")
        })
    }

    cleanDb() {
        this.makeRequest({
            url: "/clean_db",
            onSuccess: () => alert("База данных успешно очищена"),
            onError: () => alert("Ошибка очистки базы данных")
        })
    }

    makeRequest({ url, options = {}, onSuccess = () => {}, onError }) {
        fetch(url, options)
            .then((response) => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newContentWrapper = doc.querySelector(".content-wrapper");
                this.contentWrapper.innerHTML = newContentWrapper.innerHTML;
                onSuccess();
            })
            .catch(() => onError())
    }
}

new Main();
