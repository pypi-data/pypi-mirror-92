console.log("Input script loaded");

$(document).ready(function () {
    let all_inputs = $(".input-group input");
    console.log("Splitted inputs loaded.")
    if (!window.clear_splitted_inputs) {
        console.log("Splitted inputs won't be cleared.")
    } else {
        all_inputs.each(function (count, obj) {
            $(obj).val("");
        })
        console.log("Splitted inputs have been cleared.")
    }
    all_inputs.keyup(function (e) {
        let target = $(e.target);
        let value = target.val();
        let max_len = target.attr("maxLength");
        if (value.length >= max_len) {
            target.next("input").focus();
            console.log("Next target selected");
        }
    })
})