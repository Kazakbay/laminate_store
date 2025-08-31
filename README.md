# Laminate Store 🛒

A prototype online store for a laminate shop, built with **FastAPI**, **JavaScript**, **HTML**, and **CSS**.  
This project is a learning/practice project to showcase backend + frontend integration.

---

## 🚀 Features
- 🛍️ Add and display products (name, price, image)  
- 📂 File uploads (product images)  
- 📄 Dynamic frontend with HTML, CSS, and JavaScript  
- ⚡ Backend powered by FastAPI  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, SQLAlchemy  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL (can be swapped with SQLite for testing)  

---

## 📂 Project Structure
```
laminate_store/
│── main.py              # FastAPI entry point
│── requirements.txt     # Project dependencies
│── README.md            # Project description
│── .gitignore           # Ignored files & folders
│
├── static/              # Frontend assets
│   ├── style.css
│   └── script.js
│
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_product.html
│   ├── admin.html
│   ├── cart.html
│   └── order.html
│
├── uploads/             # Uploaded product images
│
└── screenshots/         # Project screenshots (for README)
```
## 📦 Installation & Setup

Clone the repository:
```bash
git clone https://github.com/Kazakbay/laminate_store.git
cd laminate_store
