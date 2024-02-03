$("#shareCorporationModal").on("show.bs.modal", function (e) {
    // Button that triggered the modal.
    var button = $(e.relatedTarget);

    // Extract info from data-* attributes.
    var corporation_id = button.data("corporation-number");
    var corporation_url = window.location.origin + button.data("corporation-url");
    var corporation_name = button.data("corporation-name");

    // Get the modal.
    var modal = $(this);

    // Set the title of the modal.
    modal.find(".modal-title").text("Share " + corporation_name + " (ID: " + corporation_id + ")");

    // Set the href of the share buttons.
    modal.find(".modal-body #share-in-telegram").attr("href", "https://t.me/share/url?url=" + corporation_url);
    modal.find(".modal-body #share-in-whatsapp").attr("href", "https://api.whatsapp.com/send?text=" + corporation_url);
    modal.find(".modal-body #share-in-facebook").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + corporation_url);
    modal.find(".modal-body #share-in-twitter").attr("href", "https://twitter.com/intent/tweet?url=" + corporation_url);

    // Set the value of the input field.
    modal.find("#share-link").val(corporation_url);
    // Copy the link to clipboard.
    var copyText = document.getElementById("share-link");
    modal.find("#copy-link").click(function () {
        copyText.select();
        document.execCommand("copy");
    });
});
