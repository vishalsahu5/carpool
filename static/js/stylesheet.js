window.onload = function () {
    var header = document.getElementById('header');
    var pictures = ['https://newevolutiondesigns.com/images/freebies/winter-facebook-cover-preview-4.jpg','https://newevolutiondesigns.com/images/freebies/winter-facebook-cover-preview-5.jpg','https://newevolutiondesigns.com/images/freebies/winter-facebook-cover-preview-7.jpg','https://newevolutiondesigns.com/images/freebies/winter-facebook-cover-preview-10.jpg','https://newevolutiondesigns.com/images/freebies/winter-facebook-cover-preview-13.jpg'];
    var numPics = pictures.length;
    if (document.images) {
        var chosenPic = Math.floor((Math.random() * numPics));
        header.style.background = 'url(' + pictures[chosenPic] + ')';
    }
};