# Phimart E-commerce API

Phimart E-commerce API is a **production-oriented RESTful backend** built with **Django Rest Framework (DRF)**. The project is designed following clean backend principles, proper separation of concerns, and scalable API practices. It supports **JWT-based authentication & authorization using Djoser**, and provides a full-featured backend for a modern e-commerce system. API contracts are documented using **Swagger (drf-yasg)**.

---

## 🚀 Key Highlights

* Industry-standard RESTful API design
* JWT Authentication & Authorization (Djoser)
* Role-based permission system (Admin / User)
* Modular & scalable project structure
* Secure cart & order lifecycle handling
* Auto-generated Swagger & ReDoc documentation
* Ready for frontend or mobile app integration

---

## 🧩 Core Features

### 🔐 Authentication & Authorization

* User Registration & Login
* JWT Access & Refresh Token support
* Token verification & refresh flow
* Permission-based access control

### 🛍️ Product Management

* Product listing & detail view
* Category-based organization
* Admin-only product & category CRUD

### 🛒 Cart System

* User-specific cart
* Add / update / remove cart items
* Real-time cart total calculation

### 📦 Order System

* Order creation from cart
* Order status management
* User order history
* Admin-level order control

---

## 🏗️ Architecture Overview

The project follows a **layered backend architecture**:

* **Models Layer** → Database schema & relations
* **Serializers Layer** → Validation & data transformation
* **Service Layer** → Business logic abstraction
* **Views / ViewSets** → Request–response handling
* **Permissions Layer** → Access control rules

This approach improves:

* Code readability
* Testability
* Long-term maintainability

---

## 🛠️ Tech Stack

| Component | Technology                    |
| --------- | ----------------------------- |
| Language  | Python 3                      |
| Framework | Django, Django Rest Framework |
| Auth      | Djoser + JWT                  |
| Database  | SQLite / PostgreSQL           |
| Docs      | drf-yasg (Swagger, ReDoc)     |
| API Style | REST                          |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/phimart-ecommerce-api.git
cd phimart-ecommerce-api
```

### 2️⃣ Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
# Windows
venv\\Scripts\\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Configuration

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

### 5️⃣ Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

### 7️⃣ Run Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication Strategy

The API uses **JWT-based stateless authentication** implemented via **Djoser**.

Authentication is designed to be secure, scalable, and frontend-agnostic, making it suitable for web, mobile, and third-party client consumption.

All request authorization is handled through standard HTTP headers using bearer tokens.

http
Authorization: Bearer, JWT <access_token>

```

---

## 📡 API Versioning

All endpoints are versioned to ensure **backward compatibility** and future scalability.

**Base URL:**
```

/api/v1/

```

This allows introducing newer versions (`v2`, `v3`, etc.) without breaking existing clients.

---


## 📑 API Documentation

- **Swagger UI:**
```

[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

```

- **ReDoc:**
```

[http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

```

---

## 🔒 Security Considerations

- JWT-based stateless authentication
- Permission classes for role control
- Write operations restricted to authorized users
- Admin-only sensitive endpoints

---

## 📁 Project Structure

```


````

---

## 🧪 Testing

```bash
python manage.py test
````



## 👤 Author

**Mubtasim Ahsan Taha**


---

## 📄 License

MIT License

---

