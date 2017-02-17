function addToCart(id, name, price) {
    $('#product_id').val(id);
    $('#product_name').val(name);
    $('#price').val(price);
    $('#addForm').submit();
}

function removeFromCart(id) {
    $('#product_id').val(id);
    $('#removeForm').submit();
}
