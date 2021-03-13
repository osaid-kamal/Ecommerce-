var updbtn = document.getElementsByClassName('update-cart');
for (i = 0; i < updbtn.length; i++) {
    updbtn[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        // console.log("User:" , user); 
        // if(user == "AnonymousUser"){
        //     console.log("Not logged in");
        // }
        // else{
        //     console.log("User is authenticated");
        // }
        updateorder(productId,action);
    })

}

function updateorder(productId, action) {
    console.log("User is authenticated,data processed..")
    var url = '/updateItem/';
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({'productId': productId, 'action': action })
            
            })
            .then((response) => console.log(response))
            .then((data) => {
                location.reload();
            })
    }

function addCookieItem(productId, action) {
    console.log('User is not authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }

        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload();
}