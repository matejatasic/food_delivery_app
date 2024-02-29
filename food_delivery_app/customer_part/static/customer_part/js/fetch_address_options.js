$( document ).ready(() => {
    $('.django-select2').djangoSelect2({
        minimumInputLength: 2,
        ajax: {
            url: `${route}`,
            dataType: 'json',
            data: (params) => {
                return {
                    term: params.term
                };
            },
            processResults: (data) => {
                return {
                    results: $.map(data.results, (item) => {
                        return {
                            text: item.text,
                            id: item.id
                        }
                    })
                };
            }
        }
    });
});