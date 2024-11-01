# 🛍️ Ethereum E-Commerce Extravaganza 🎉

Welcome to **Eth-Ecom!** 🎈 Where shopping meets blockchain magic! 🪄 Dive into the world of decentralized shopping with our Ethereum-powered e-commerce app built with Django, Web3.py, and Web3.js. Here, your purchases go directly from the wallet to the blockchain – no middlemen, no frills, just some serious on-chain action.

---

## 🧰 What's Inside?

A quick peek at the treasure trove:

```
eth_ecommerce/
├── eth_ecommerce/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── store/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── store/
│   │       └── product.html
│   └── utils.py
├── contracts/
│   └── ProductMarket.sol
├── manage.py
└── requirements.txt

```

---

## 🛠️ Setup Instructions (Serious Stuff)
1. Clone the repo and set up a Python virtual environment. Make sure it’s ready for some blockchain vibes.
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt

2. **Compile & Deploy** the `ProductMarket.sol` smart contract on your favorite testnet. Don’t forget to keep that contract address safe! 🗝️

3. **Set up Django** settings for Web3 and Ethereum, then run the server to launch this shopping adventure.

4. Visit [http://127.0.0.1:8000/store/product/](http://127.0.0.1:8000/store/product/) and start shopping on-chain! Testing the Application : 1. Add a Product: Enter a product name and price, then click Add Product.
	2.	Purchase a Product: Enter the product ID and click Purchase Product.

---

## 💸 How It Works (The Fun Part)

1. **Add Products**: Tell the blockchain what to sell – enter a name and price, and watch it appear like magic!
2. **Buy Products**: Connect your Ethereum wallet (yep, we’re talking Metamask!) and click buy. Watch as your funds fly through the blockchain to your new purchase.
3. **Instant Gratification? Not Quite!** Transactions will show up in the ether. Well, it *is* Ethereum after all.

---

## 🤖 Tech Stuff

- **Backend**: Django 🐍 + Web3.py for connecting to Ethereum.
- **Smart Contracts**: Solidity for product listings and payments.
- **Frontend**: Web3.js + JavaScript to link users and wallets to Ethereum.

---

## 🍿 Why We Built It

Because… Why not? Ever wondered what e-commerce would look like if it was all on-chain? Now you don’t have to. Enjoy your Ethereum shopping sprees, because Web3 just made buying online nerdier than ever! 🚀

Happy shopping! 🛒 (P.S. Don’t blame us if gas fees ruin the fun 🙈)


<img src="resources/1.png" alt="Image 1" width="450" height="550">
