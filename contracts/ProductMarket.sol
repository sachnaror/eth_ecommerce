
pragma solidity ^0.8.0;

contract ProductMarket {
    struct Product {
        uint id;
        string name;
        uint price;
        address payable owner;
        bool purchased;
    }

    mapping(uint => Product) public products;
    uint public productCount;

    event ProductCreated(uint id, string name, uint price, address owner);
    event ProductPurchased(uint id, address buyer);

    function createProduct(string memory _name, uint _price) public {
        require(_price > 0, "Price must be greater than zero");

        productCount++;
        products[productCount] = Product(productCount, _name, _price, payable(msg.sender), false);

        emit ProductCreated(productCount, _name, _price, msg.sender);
    }

    function purchaseProduct(uint _id) public payable {
        Product storage product = products[_id];
        require(_id > 0 && _id <= productCount, "Invalid product ID");
        require(msg.value == product.price, "Incorrect amount sent");
        require(!product.purchased, "Product already purchased");

        product.owner.transfer(msg.value);
        product.purchased = true;

        emit ProductPurchased(_id, msg.sender);
    }
}
