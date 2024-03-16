$(document).ready(function () {
    $('tr').each(function () {

        const family = $(this).find("#family");
        const veggie = $(this).find("#veggie");
        const options = veggie.find('option');

        family.on('change', function (event) {
            veggie.html(options.filter('[family="' + family.val() + '"]'));
        }).trigger('change');
    });
});