// Set event listener for the options checkboxes.
$(document).ready(function() {
    $(".checkbox-option-label > input").click(function() {
        // Get the label of the checkbox.
        var label = $(this).parent();

        // Get the container data-widget-id.
        var containerDataWidgetId = label.closest("div").attr("data-widget-id");

        if ($(this).is(":checked")) {
            // Add label to chosen options.
            console.log("Adding label to chosen options");
            $("[data-widget-id=\"" + containerDataWidgetId + "\"].chosen-options").append(label);

            // Update class of label (add rounded corners).
            label.addClass("rounded-pill");
            label.addClass("btn-outline-secondary");
            label.removeClass("btn-secondary");
        } else {
            // Add label to options.
            console.log("Adding label to options");

            $("div[data-widget-id=\"" + containerDataWidgetId + "\"].options").append(label);

            // Update class of label (remove rounded corners).
            label.removeClass("rounded-pill");
            label.removeClass("btn-outline-secondary");
            label.addClass("btn-secondary");
        }
    });
});
