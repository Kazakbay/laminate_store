let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(id, name, price) {
    cart.push({ id, name, price });
    localStorage.setItem("cart", JSON.stringify(cart));
    alert(name + " added to cart!");
}

function renderCart() {
    let list = document.getElementById("cart-items");
    let total = document.getElementById("cart-total");
    if (!list) return;

    list.innerHTML = "";
    let sum = 0;
    cart.forEach((item, i) => {
        let li = document.createElement("li");
        li.textContent = item.name + " - " + item.price + " ₸";
        list.appendChild(li);
        sum += item.price;
    });
    total.textContent = sum;
}

window.onload = renderCart;
