/**
 * Created by zengchunyun on 16/4/11.
 */
window.onload = rolloverInit;
function rolloverInit() {
    for (var i=0; i<document.images.length;i++) {
        if (document.images[i].parentNode.tagName == "A") {
            setupRollover(document.images[i]);
} }
}
function setupRollover(thisImage) {
    thisImage.outImage = new Image();
    thisImage.outImage.src = thisImage.src;
    thisImage.onmouseout = function() {
        this.src = this.outImage.src; }
    thisImage.overImage = new Image();
    thisImage.overImage.src = "./" + thisImage.id + "bo.jpg";
    thisImage.onmouseover = function() {
        this.src = this.overImage.src; }
}
