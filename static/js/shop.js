$('#main').on('click', '#addToCart', function (event) {
    event.preventDefault()
    const $element = $(this);
    const productID = $element.data('productId');
    addToCart(productID, $element)
});

function addToCart(productID, $element) {
    const addToCartURL = document.location.origin + `/cart/add/${productID}/`;
    const csrftoken = $("[name=csrfmiddlewaretoken]").val()
    $.ajax(addToCartURL,
        {
            type: "POST",
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function (response) {
                showPopover($element, response.message);
            }
        }
    )
}

function showPopover(element, message) {
    element.popover({
        content: message,
        placement: 'top',
        trigger: 'focus'
    });
    element.popover('show')
}