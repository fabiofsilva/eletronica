/*
 *
 * serializeALL
 * Depends: jQuery 1.4.2+
 *
 */
(function ($) {
    $.fn.serializeAll = function () {
        var inputs = this.find(':input');
        var data = {};
        $.each(inputs, function () {
            var input = $(this);
            if (input.val() != null && input.attr('name') != undefined) {
                if (/checkbox|radio/i.test(input.attr('type'))) {
                    if (input.attr('checked') != undefined) {
                        data[input.attr('name')] = input.val();
                    }
                } else {
                    data[input.attr('name')] = input.val();
                }
            }
        });
        return data;
    };
}(jQuery));