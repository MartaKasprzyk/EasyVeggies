$(document).ready(function () {
    $('tr').each(function () {

        const prevFamily = $(this).find("#prev_family");
        const family = $(this).find("#family");
        const veggie = $(this).find("#veggie");
        const veggieOptions = veggie.find('option');
        const familyOptions = family.find('option');

        family.on('change', function (event) {
            veggie.html(veggieOptions.filter('[family="' + family.val() + '"]'));
        }).trigger('change');

        prevFamily.on('change', function (event) {
            let previous = parseInt(prevFamily.val());
            switch (previous) {
                case 1:
                    family.html(familyOptions.filter('[family="2"], [family="3"]'));
                    break;
                case 2:
                case 3:
                    family.html(familyOptions.filter('[family="4"], [family="5"]'));
                    break;
                case 4:
                case 5:
                    family.html(familyOptions.filter('[family="6"]'));
                    break
                case 6:
                    family.html(familyOptions.filter('[family="7"]'));
                    break
                case 7:
                    family.html(familyOptions.filter('[family="1"]'));
                    break;
                default:
                    family.html(null);
            }
            family.trigger('change');
        }).trigger('change');
    });
});