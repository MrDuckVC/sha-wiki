var favoriteCorpsCookieKey = "favoriteCorps";
var favoriteCorpsButtonClass = "favorite-button";
var favoriteCorpsButtonIdPrefix = "favorite-button-";


function setFavoriteCorpIcon(corpNumber, isFavorite) {
    var corpNumberSelector = "#" + favoriteCorpsButtonIdPrefix + corpNumber;
    if (isFavorite) {
        $(corpNumberSelector).html("<i class=\"bi bi-star-fill\"></i>");
    } else {
        $(corpNumberSelector).html("<i class=\"bi bi-star\"></i>");
    }
}

function addFavoriteCorps(corpNumber) {
    // Get favorite corps.
    var corpNumbers = getFavoritesCorps();

    // Add the corp to the list.
    if (corpNumbers == []) {
        corpNumbers = [corpNumber];
    } else {
        corpNumbers.push(corpNumber);
    }

    // Save the list.
    document.cookie = favoriteCorpsCookieKey + "=" + corpNumbers + ";path=/";

    // Update the UI.
    setFavoriteCorpIcon(corpNumber, true);
}

function removeFavoriteCorps(corpNumber) {
    var corpNumbers = getFavoritesCorps();
    var index = corpNumbers.indexOf(corpNumber);
    if (index > -1) {
        corpNumbers.splice(index, 1);
    }
    document.cookie = favoriteCorpsCookieKey + "=" + corpNumbers + ";path=/";
    setFavoriteCorpIcon(corpNumber, false);
}

function getFavoritesCorps() {
    var name = favoriteCorpsCookieKey + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = document.cookie.split(";");
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length).split(",");
        }
    }
    return [];
}

$(document).ready(function() {
    // Set listeners for all favorite buttons.
    var favoriteButtons = document.getElementsByClassName(favoriteCorpsButtonClass);
    for (var i = 0; i < favoriteButtons.length; i++) {
        favoriteButtons[i].addEventListener("click", function() {
            var corpNumber = this.id.substring(favoriteCorpsButtonIdPrefix.length);
            console.log("Clicked favorite button for corp " + corpNumber);

            // Toggle the favorite status.
            if (getFavoritesCorps().includes(corpNumber)) {
                console.log("Removing corp " + corpNumber + " from favorites.");
                removeFavoriteCorps(corpNumber);
            } else {
                console.log("Adding corp " + corpNumber + " to favorites.");
                addFavoriteCorps(corpNumber);
            }
        });
    }

    // Set the favorite icons.
    var favoriteCorps = getFavoritesCorps();
    for (var i = 0; i < favoriteCorps.length; i++) {
        console.log("Setting favorite icon for corp " + favoriteCorps[i]);
        setFavoriteCorpIcon(favoriteCorps[i], true);
    }
});
