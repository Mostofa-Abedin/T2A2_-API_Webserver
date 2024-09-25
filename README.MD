# Coder Academy - Assignment T2A2 - API Webserver Project.

# Table of Contents

- [Overview](#overview)

  - [Purpose of the API](#purpose-of-the-api)
  - [Problem Statement](#problem-statement)

- [API Specifications](#api-specifications)

  - [Base URL](#base-url)
    - [Customizing the Base URL](#customizing-the-base-url)
  - [Authentication & Authorization](#authentication--authorization)
    - [Registration](#registration)
    - [JWT Authentication Process](#jwt-authentication-process)
    - [Role-Based Access Control](#role-based-access-control)
  - [Supported Formats](#supported-formats)
    - [JSON Request/Response Format](#json-requestresponse-format)
  - [HTTP Methods & Verbs](#http-methods--verbs)

- [Endpoints](#endpoints)

  - [Detailed Endpoints Reference](#detailed-endpoints-reference)
    - [User Endpoints](#user-endpoints)
    - [Car Endpoints](#car-endpoints)
    - [Make Model Year Endpoints](#make-model-year-endpoints)
    - [Listing Endpoints](#listing-endpoints)
    - [Car Transaction Endpoints](#car-transaction-endpoints)
  - [Summary of Endpoints](#summary-of-endpoints)

- [Data Model](#data-model)

  - [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
  - [ORM Explanation](#orm-explanation)
  - [Database System](#database-system)
  - [Normalization of Tables](#normalization-of-tables)
  - [Data Models (Entities)](#data-models-entities)
    - [User Model](#user-model)
    - [Car Model](#car-model)
    - [Listing Model](#listing-model)
    - [CarTransaction Model](#cartransaction-model)
    - [MakeModelYear Model](#makemodelyear-model)

- [Error Handling & Status Codes](#error-handling--status-codes)

  - [Standard HTTP Status Codes](#standard-http-status-codes)
  - [Custom Error Messages For Developer Debugging](#custom-error-messages-for-developer-debugging)

- [Security](#security)

  - [JWT Token Security](#jwt-token-security)
  - [Best Practices for Securing API Keys](#best-practices-for-securing-api-keys)

- [Testing](#testing)

  - [Using Insomnia for Manual Testing](#using-insomniapostman-for-manual-testing)

- [Local Setup & Developer Utilities](#local-setup--developer-utilities)

  - [Local Setup and Running Flask ](#local-setup-and-running-flask)
  - [CLI controllers ](#cli-controllers)
  - [PostgreSQL Setup](#postgresql-setup)

- [Project Management](#project-management)

  - [Project Timeline](#project-timeline)
  - [Sprint Planning & Milestones](#sprint-planning--milestones)
    - [Epics and User Stories](#epics-and-user-stories)
    - [Task Breakdown and Assignments](#task-breakdown-and-assignments)
  - [Jira/Project Management Tools Used](#jiraproject-management-tools-used)
    - [Jira Boards and Tracking](#jira-boards-and-tracking)

---

# Overview

This README serves as the technical documentation for the **Car Marketplace API**, a RESTful web service built to facilitate transactions for buying, selling, and managing cars in an online marketplace. The API provides endpoints for user management, car listings, transactions, and more.

---

## Purpose of the API

The **Car Marketplace API** serves as the backend infrastructure that developers can leverage to build a comprehensive two-sided car marketplace. This API has strategic endpoints that are well-structured to handle typical car marketplace CRUD interactions such as user authentication, car listing management, secure transactions, and user roles. Developers may use this API to integrate with front-end platforms or mobile applications to create a fully functional car marketplace.

Furthermore, this API is developed as part of a web server development assignment at Coder Academy. It is designed to allow students to showcase their core competencies in API design, authentication, and database management.

---

## Problem Statement

The used car market is predominantly an online affair these days. 80% of car buyers conducting research online before making a purchase decision (Cox Automotive, 2023). Moreover, 67% of buyers prefer an online platform to handle the majority of the purchasing process (Autotrader 2022)

However, as with most platforms of commerce, the online car marketplace also has gaps in efficient and scalable platforms that manage the entire lifecycle of car transactions, from listing a vehicle to completing the sale.

The **Car Marketplace API** addresses this problem by:

- Enabling secure and authenticated transactions between buyers and sellers.
- Allowing sellers to manage their car listings easily.
- Providing buyers with accurate and up-to-date information on available cars.
- Offering administrative control for managing users, cars, and transactions.

**Example Use Case:**

A seller has bought a new vehicle and would like to quickly and securely list their old car for sale. Using a front end built upon this API, the seller could list their car for sale. Using the API’s secure authentication system, they can create an account, upload vehicle details, and monitor offers. Buyers, in turn, can browse listings, negotiate prices, and complete secure transactions, all within a single integrated platform.

**References:**
Cox Automotive, 2023. Car Buyer Journey Report. [online] Available at: https://www.coxautoinc.com/market-insights/car-buyer-journey/ [Accessed 22 Sep. 2024].

Autotrader, 2022. The Digital Future of Automotive Retail. [online] Available at: https://www.autotrader.com/car-news/digital-future-automotive-retail-report [Accessed 22 Sep. 2024].

---

# API Specifications

For **SETUP** see section **[Local Setup & Developer Utilities](#local-setup--developer-utilities)**

## Base URL

The base URL for accessing the Car Marketplace API is:

```bash
http://localhost:8080/api
```

All API endpoints are prefixed with /api, and specific resources such as users, cars, and listings can be accessed via their respective paths.

### Customizing the Base URL

To modify the base URL or database connection settings for your environment (e.g., development, testing, or production), you can use the .env file.

- **Step 1:** In the project root, you will find a .env.example file that serves as a template for setting up your environment variables.
- **Step 2:** Create a copy of this file and name it .env.
- **Step 3:** Update the variables within .env to match your specific setup.

For example:

```bash
DATABASE_URL = "postgresql+psycopg2://car_market_dev:123456@localhost:5432/car_market"
JWT_SECRET_KEY = "YourSecretKey"
```

## Authentication & Authorization

The Car Marketplace API uses JWT (JSON Web Token) for user authentication and role-based access control. To access the majority of the API's functionalities, authentication is required and users need to include their token in the Authorization header when making requests

### Registration

Users are required to register themselves in the system before they are provided with a JWT.

1. **User Registration:** A new user must provide their details for registration. Details like name, email, password, phone number and address need to be provided via the registration endpoint. Upon successful registration, the user can log in.

**Endpoint:** POST /api/register Request Body:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "yourpassword",
  "phone_number": "1234567890",
  "address": "123 Main St"
}
```

**Response:**

```json
{
  "message": "User registered successfully"
}
```

### JWT Authentication Process

1. **User Login:** To authenticate a user must begin by providing their credentials (email and password) via the login endpoint. Upon successful authentication, the API returns a JWT.

**Endpoint:** POST /api/login Request Body:

```json
{
  "email": "john@example.com",
  "password": "yourpassword"
}
```

**Response:**

```json
{
  "token": "your.jwt.token"
}
```

2. **Token Usage:** The user includes the JWT in the header of subsequent requests using the Authorization header in this format:

```makefile
Authorization: Bearer <JWT>
```

3. **Token Expiry:** Tokens have a limited lifespan for security purposes. If the token expires, users will need to log in again to obtain a new token.

4. **Token Validation:** All protected endpoints check for a valid JWT before processing the request. Unauthorized users will receive a 401 Unauthorized response if the token is missing or invalid.

### Role-Based Access Control

The Car Marketplace API enforces role-based access control (RBAC) with the following roles:

- **Admin:** Can manage users, cars, and listings. Has full access to all endpoints.
- **Standard User:** Can create, read, update, and delete their own listings and transactions.

Depending on the user’s role, they will have different levels of access to the API’s resources. Admin users have broader control, including deleting users and managing all listings.

## Supported Formats

The **Car Marketplace API** primarily uses JSON (JavaScript Object Notation) as the standard format for both requests and responses. JSON is widely used in API projects because it is lightweight, human-readable and ease of integration with various programming languages.

### JSON Request/Response Format

All API requests to the **Car Marketplace API** must be made in JSON format, the server will also respond with JSON-encoded data. This format ensures seamless data exchange between client and server. Please ensure the Content-Type header is set to application/json for all POST, PUT, and PATCH requests.

```bash
Content-Type: application/json
Accept: application/json
```

An example of Request and Response format is given below.

**Example Request:**

```json
POST /api/listings
{
  "car_id": 1,
  "price": 25000,
  "listing_status": "available"
}
```

**Example Response:**

```json
{
  "listing_id": 5,
  "car_id": 1,
  "price": 25000,
  "listing_status": "available",
  "date_posted": "2024-09-22"
}
```

## HTTP Methods & Verbs

The **Car Marketplace API** supports several HTTP methods (also known as verbs), each corresponding to a different type of operation. These methods adhere to RESTful API principles.

| **HTTP Method** | **Description**                                                                      |
| --------------- | ------------------------------------------------------------------------------------ |
| **GET**         | Retrieves data from the server without altering the server's state.                  |
| **POST**        | Submits data to the server, which usually results in the creation of a new resource. |
| **PUT**         | Replaces the entire representation of the targeted resource with the data provided.  |
| **PATCH**       | Partially updates a resource by modifying only specific fields.                      |
| **DELETE**      | Removes the specified resource from the server.                                      |

---

# Endpoints

## Detailed Endpoints Reference

### User Endpoints

#### `POST /api/register`

- **Description:** This endpoint registers a new user. The user must provide a valid email, password, name, and optionally phone number and address.
- **Allowed Fields:**
  - **Required:**
    - **email:** `VARCHAR(50)`, unique, not null.
    - **password:** `VARCHAR(200)`, not null.
    - **name:** `VARCHAR(100)`, not null.
  - **Optional:**
    - **phone_number:** `VARCHAR(15)`, can include symbols like `+`.
    - **address:** `VARCHAR(255)`
- **Restrictions:**
  - The email must be unique.
  - The password must meet security requirements (e.g., length between 8-20 characters).
  - Only non-admin users can be created here (admin roles must be assigned manually).
- **Example Request:**

```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "phone_number": "+1234567890",
  "address": "123 Example Street"
}
```

- **Example Response:**

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "user@example.com",
  "is_admin": false
}
```

#### `POST /api/login`

- **Description:** This endpoint authenticates a user and generates a JWT token.
- **Allowed Fields:**
  - **Required:**
    - email: `VARCHAR(50)`, not null.
    - password: `VARCHAR(200)`, not null.
- **Restrictions:**
  - The user must already be registered.
  - The password must match the hashed password stored in the database.
- **Example Request:**

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

- **Example Response:**

```json
{
  "token": "JWT token here",
  "email": "user@example.com",
  "is_admin": false
}
```

#### `PUT /api/users/<id>`(also supports PATCH)

- **Description:** This endpoint allows users to update their own profile or admins to update any user’s profile.

- **Allowed Fields:**
  - **Optional**
    - email: `VARCHAR(50)`, unique.
    - password: `VARCHAR(200)`, must meet security requirements.
    - name: `VARCHAR(100)`
    - phone_number: `VARCHAR(15)`
    - address: `VARCHAR(255)`
- **Restrictions:**

  - Only admins can update other users' profiles.
  - Non-admin users can only update their own profile.

- **Example Request:**

```json
{
  "name": "Updated Name",
  "email": "updated_email@example.com"
}
```

- **Example Response:**

```json
{
  "user_id": 1,
  "name": "Updated Name",
  "email": "updated_email@example.com",
  "is_admin": false
}
```

#### `DELETE /api/users/<id>`

- **Description:** This endpoint allows admins to delete a user from the system.
- **Restrictions:**
  - Only admin users can delete other users.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "message": "User deleted successfully."
}
```

- **Description:**

- **Allowed Fields:**
  - **Required:**
  - **Optional**
- **Restrictions:**
- **Example Request:**
- **Example Response:**

### Car Endpoints

#### `GET /api/cars`

- **Description:** Retrieves a list of all cars in the marketplace. No authentication is required.

- **Restrictions:**
  - The endpoint is publicly accessible.
  - Pagination or filtering might be available based on additional features.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
[
  {
    "car_id": 1,
    "mileage": 50000,
    "price": 15000.0,
    "condition": "used",
    "description": "Well-maintained car with low mileage",
    "image_url": "http://example.com/car1.jpg",
    "make_model_year": {
      "make": "Toyota",
      "model": "Corolla",
      "year": 2018
    }
  },
  {
    "car_id": 2,
    "mileage": 10000,
    "price": 25000.0,
    "condition": "new",
    "description": "Brand new car with advanced features",
    "image_url": "http://example.com/car2.jpg",
    "make_model_year": {
      "make": "Honda",
      "model": "Civic",
      "year": 2020
    }
  }
]
```

#### `GET /api/cars/<id>`

- **Description:** Retrieves a specific car by its ID.

- **Allowed Fields:**
  - No request fields are necessary; the car's ID is provided in the URL path.
- **Restrictions:**
  - This endpoint is publicly accessible.
  - Returns 404 if the car is not found.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "car_id": 1,
  "mileage": 50000,
  "price": 15000.0,
  "condition": "used",
  "description": "Well-maintained car with low mileage",
  "image_url": "http://example.com/car1.jpg",
  "make_model_year": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2018
  }
}
```

#### `POST /api/cars`

- **Description:** Creates a new car in the marketplace. Only admins can create cars.

- **Allowed Fields:**
  - **Required:** `mileage, price, condition, make_model_year_id`
  - **Optional:** `description, image_url`
- **Restrictions:**
- This endpoint requires admin authentication.
- The `make_model_year_id` must reference a valid make, model, and year.
- The `condition` field must be one of: `new`, `used`, or `certified`.
- **Example Request:**

```json
{
  "mileage": 50000,
  "price": 15000.0,
  "condition": "used",
  "description": "Well-maintained car with low mileage",
  "image_url": "http://example.com/car1.jpg",
  "make_model_year_id": 1
}
```

- **Example Response:**

```json
{
  "car_id": 1,
  "mileage": 50000,
  "price": 15000.0,
  "condition": "used",
  "description": "Well-maintained car with low mileage",
  "image_url": "http://example.com/car1.jpg",
  "make_model_year": {
    "make_model_year_id": 1,
    "make": "Toyota",
    "model": "Corolla",
    "year": 2018
  }
}
```

#### `PUT /api/cars/<id>`

- **Description:** Updates an existing car by replacing all details with new values. Admin access is required.

- **Allowed Fields:**
  - **Required:** `mileage`, `price`, `condition`, `make_model_year_id`
  - **Optional:** `description`, `image_url`
- **Restrictions:**
  - Only an admin can perform this operation.
  - The make_model_year_id must reference an existing make, model, and year.
  - Any associated listings or transactions are not modified by this update.
- **Example Request:**

```json
{
  "mileage": 60000,
  "price": 14000.0,
  "condition": "used",
  "description": "Updated description for the car",
  "image_url": "http://example.com/car1_updated.jpg",
  "make_model_year_id": 2
}
```

- **Example Response:**

```json
{
  "car_id": 1,
  "mileage": 60000,
  "price": 14000.0,
  "condition": "used",
  "description": "Updated description for the car",
  "image_url": "http://example.com/car1_updated.jpg",
  "make_model_year": {
    "make_model_year_id": 2,
    "make": "Honda",
    "model": "Civic",
    "year": 2019
  }
}
```

#### `PUT /api/cars/<id>`

- **Description:** Partially updates a car's information, allowing specific fields to be modified without replacing the entire resource.

- **Allowed Fields:**
  - **Optional:** `mileage`, `price`, `condition`, `description`, `image_url`, `make_model_year_id`
- **Restrictions:**
  - Admin access is required.
  - Only the fields provided in the request body will be updated.
- **Example Request:**

```json
{
  "price": 13000.0,
  "condition": "certified"
}
```

- **Example Response:**

```json
{
  "car_id": 1,
  "mileage": 50000,
  "price": 13000.0,
  "condition": "certified",
  "description": "Well-maintained car with low mileage",
  "image_url": "http://example.com/car1.jpg",
  "make_model_year": {
    "make_model_year_id": 1,
    "make": "Toyota",
    "model": "Corolla",
    "year": 2018
  }
}
```

#### `DELETE /api/cars/<id>`

- **Description:** Deletes a car by its ID. Admin access is required. Cars with associated transactions cannot be deleted.

- **Allowed Fields:**
  - No fields are required in the request body, but the car's ID is included in the URL path.
- **Restrictions:**
  - Only admins can delete cars.
  - A car cannot be deleted if it has associated transactions.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "message": "Car deleted successfully."
}
```

### Make Model Year Endpoints

#### `GET /api/makemodelyears`

- **Description:** Retrieves a list of all car make, model, and year combinations.

- **Allowed Fields:**
  - No input fields required for this request.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
[
  {
    "make_model_year_id": 1,
    "make": "Toyota",
    "model": "Corolla",
    "year": 2020
  },
  {
    "make_model_year_id": 2,
    "make": "Honda",
    "model": "Civic",
    "year": 2019
  }
]
```

#### `GET /api/makemodelyears/<id>`

- **Description:** Retrieves a specific make, model, and year entry by its ID.

- **Allowed Fields:**
  - No input fields required for this request.
- **Restrictions:**
  - The `id` must correspond to an existing make, model, and year combination.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "make_model_year_id": 1,
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020
}
```

#### `POST /api/makemodelyears`

- **Description:** Creates a new make, model, and year entry.

- **Allowed Fields:**
  - **Required:**
    - make (VARCHAR, max length 100, not null)
    - model (VARCHAR, max length 100, not null)
    - year (INT, not null).
- **Restrictions:**
  - The make and model fields must be strings and should not exceed 100 characters.
  - The year must be a valid integer (e.g., 2020).
- **Example Request:**

```json
{
  "make": "Ford",
  "model": "Mustang",
  "year": 2021
}
```

- **Example Response:**

```json
{
  "make_model_year_id": 3,
  "make": "Ford",
  "model": "Mustang",
  "year": 2021
}
```

#### `PUT /api/makemodelyears/<id>`

- **Description:** Updates an existing make, model, and year entry by its ID

- **Allowed Fields:**
  - **Required:**
    - make (VARCHAR, max length 100, not null)
    - model (VARCHAR, max length 100, not null)
    - year (INT, not null).
- **Restrictions:**
  - The make and model fields must be strings and should not exceed 100 characters.
  - The year must be a valid integer (e.g., 2020).
  - The id must correspond to an existing make, model, and year combination.
- **Example Request:**

```json
{
  "make": "Ford",
  "model": "Mustang",
  "year": 2022
}
```

- **Example Response:**

```json
{
  "make_model_year_id": 3,
  "make": "Ford",
  "model": "Mustang",
  "year": 2022
}
```

#### `DELETE /api/makemodelyears/<id>`

**Description:** Deletes a specific make, model, and year entry by its ID.

- **Restrictions:**
  - The id must correspond to an existing make, model, and year combination.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "message": "Make, model, and year combination deleted successfully."
}
```

### Listing Endpoints

#### `GET /api/listings`

- **Description:** This endpoint retrieves all car listings.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
[
  {
    "listing_id": 1,
    "car_id": 1,
    "seller_id": 2,
    "listing_status": "available",
    "date_posted": "2024-09-22",
    "car": {
      "make_model_year": {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2020
      },
      "price": 20000,
      "mileage": 15000,
      "condition": "used"
    }
  }
]
```

#### `GET /api/listings/<id>`

- **Description:** This endpoint retrieves a specific car listing by its ID.
- **Restrictions:**
  - The listing must exist.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "listing_id": 1,
  "car_id": 1,
  "seller_id": 2,
  "listing_status": "available",
  "date_posted": "2024-09-22",
  "car": {
    "make_model_year": {
      "make": "Toyota",
      "model": "Corolla",
      "year": 2020
    },
    "price": 20000,
    "mileage": 15000,
    "condition": "used"
  }
}
```

#### `POST /api/listings`

- **Description:** This endpoint creates a new car listing. The listing will default to "available" status and is linked to the authenticated user as the seller.

- **Allowed Fields:**
  - **Required:** `car_id`
  - **Auto-generated:** `listing_status`, `date_posted`
- **Restrictions:**
  - Only authenticated users can create listings.
  - The car_id must exist.
  - A car can only have one active listing.
- **Example Request:**

```json
{
  "car_id": 1
}
```

- **Example Response:**

```json
{
  "listing_id": 1,
  "car_id": 1,
  "seller_id": 2,
  "listing_status": "available",
  "date_posted": "2024-09-22"
}
```

#### `PUT /api/listings/<id>`

- **Description:** This endpoint updates an existing car listing with new details.

- **Allowed Fields:**
  - **Optional:** `listing_status`
- **Restrictions:**
  - The listing must exist.
  - Only the seller or an admin can update the listing.
- **Example Request:**

```json
{
  "listing_status": "sold"
}
```

- **Example Response:**

```json
{
  "listing_id": 1,
  "car_id": 1,
  "seller_id": 2,
  "listing_status": "sold",
  "date_posted": "2024-09-22"
}
```

#### `DELETE /api/listings/<id>`

- **Description:** This endpoint deletes a car listing.
- **Restrictions:**
  - The listing must exist.
  - Only the seller or an admin can delete the listing.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "message": "Listing deleted successfully."
}
```

### Car Transaction Endpoints

#### `GET /api/car-transactions`

- **Description:** Retrieve all car transactions.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
[
  {
    "transaction_id": 1,
    "car_id": 1,
    "buyer_id": 2,
    "transaction_date": "2024-09-20",
    "amount": 20000.0
  }
]
```

#### `GET /api/car-transactions/<id>`

- **Description:** Retrieve a specific car transaction by its ID.

- **Allowed Fields:**
  - **Required:** `transaction_id` must be a valid integer
- **Restrictions:**
  - The transaction ID must exist in the system.
- **Example Request:**

```json
(No body required)
```

- **Example Response:**

```json
{
  "transaction_id": 1,
  "car_id": 1,
  "buyer_id": 2,
  "transaction_date": "2024-09-20",
  "amount": 20000.0
}
```

#### `POST /api/car-transactions`

- **Description:** Create a new car transaction. This endpoint allows a user to purchase a car, given that the car is available, and processes the transaction.

- **Allowed Fields:**
  - **Required:**
    - car_id: INT, FK referencing cars.car_id. Not Null
    - buyer_id: INT, FK referencing users.user_id. Not Null
    - amount: FLOAT, must be non-negative. Not Null
    - transaction_date: DATE, automatically set to the current date. Not Null
- **Restrictions:**
  - The car must have a status of `available` in the LISTINGS table.
  - The amount field should match the listed price of the car
- **Example Request:**

```json
{
  "car_id": 1,
  "amount": 20000.0
}
```

- **Example Response:**

```json
{
  "transaction_id": 1,
  "car_id": 1,
  "buyer_id": 2,
  "transaction_date": "2024-09-20",
  "amount": 20000.0
}
```

## Summary of Endpoints

### User Endpoints

| Endpoint              | Method     | Description                                 | Admin Only       |
| --------------------- | ---------- | ------------------------------------------- | ---------------- |
| `/api/register`       | POST       | Register a new user.                        | No               |
| `/api/login`          | POST       | Authenticate a user and return a JWT token. | No               |
| `/api/users/<int:id>` | PUT, PATCH | Update user information (Admin or self).    | Yes (for others) |
| `/api/users/<int:id>` | DELETE     | Delete a user.                              | Yes              |

### Car Endpoints

| Endpoint             | Method     | Description                        | Admin Only |
| -------------------- | ---------- | ---------------------------------- | ---------- |
| `/api/cars`          | GET        | Retrieve a list of all cars.       | No         |
| `/api/cars/<int:id>` | GET        | Retrieve a specific car by its ID. | No         |
| `/api/cars`          | POST       | Create a new car.                  | Yes        |
| `/api/cars/<int:id>` | PUT, PATCH | Update an existing car.            | Yes        |
| `/api/cars/<int:id>` | DELETE     | Delete a car by its ID.            | Yes        |

### Listing Endpoints

| Endpoint                 | Method     | Description                      | Admin Only       |
| ------------------------ | ---------- | -------------------------------- | ---------------- |
| `/api/listings`          | GET        | Retrieve all car listings.       | No               |
| `/api/listings/<int:id>` | GET        | Retrieve a specific car listing. | No               |
| `/api/listings`          | POST       | Create a new car listing.        | No               |
| `/api/listings/<int:id>` | PUT, PATCH | Update an existing car listing.  | No (Owner/Admin) |
| `/api/listings/<int:id>` | DELETE     | Delete a car listing by its ID.  | No (Owner/Admin) |

### Car Transaction Endpoints

| Endpoint                         | Method | Description                                    | Admin Only |
| -------------------------------- | ------ | ---------------------------------------------- | ---------- |
| `/api/car-transactions`          | GET    | Retrieve all car transactions.                 | No         |
| `/api/car-transactions/<int:id>` | GET    | Retrieve a specific car transaction by its ID. | No         |
| `/api/car-transactions`          | POST   | Create a new car transaction.                  | No         |

### MakeModelYear Endpoints

| Endpoint                      | Method     | Description                            | Admin Only |
| ----------------------------- | ---------- | -------------------------------------- | ---------- |
| `/api/makemodelyear`          | GET        | Retrieve all makes, models, and years. | No         |
| `/api/makemodelyear/<int:id>` | GET        | Retrieve a specific make/model/year.   | No         |
| `/api/makemodelyear`          | POST       | Create a new make/model/year entry.    | Yes        |
| `/api/makemodelyear/<int:id>` | PUT, PATCH | Update an existing make/model/year.    | Yes        |
| `/api/makemodelyear/<int:id>` | DELETE     | Delete a make/model/year entry.        | Yes        |

---

# Data Model

## Entity Relationship Diagram (ERD)

The Entity Relationship Diagram (ERD) below illustrates how the different models in the Car Marketplace API database interact with each other. Each table has connections with other tables that facilitate the complex interactions of a car marketplace.

**Diagram Overview:**

- The **USERS** table is connected to **LISTINGS** and **TRANSACTIONS**, showing that users can create listings and engage in transactions.

- **CARS** are listed by users in the **LISTINGS** table, and the transactions involving cars are stored in the **TRANSACTIONS** table.

- The **MAKEMODELYEAR** table holds information about the make, model, and year of cars, referenced by the **CARS** table.

```mermaid
erDiagram
    USERS {
        user_id INT PK
        name VARCHAR(100)
        email VARCHAR(50) UK
        password VARCHAR(255)
        phone_number VARCHAR(15)
        address VARCHAR(255)
    }

    CARS {
        car_id INT PK
        make_model_year_id INT FK
        mileage INT
        price FLOAT
        condition ENUM
        description VARCHAR(1000)
        image_url VARCHAR(100)
    }

    MAKEMODELYEAR {
        make_model_year_id INT PK
        make VARCHAR(100)
        model VARCHAR(100)
        year INT
    }

    LISTINGS {
        listing_id INT PK
        car_id INT FK
        seller_id INT FK
        listing_status VARCHAR
        date_posted DATE
    }

    TRANSACTIONS {
        transaction_id INT PK
        buyer_id INT FK
        car_id INT FK
        transaction_date DATE
        amount FLOAT
    }

    CARS ||--o{ LISTINGS : "is listed in"
    CARS ||--o{ TRANSACTIONS : "is sold in"
    CARS }o--|| MAKEMODELYEAR : "references"

    USERS ||--o{ LISTINGS : "creates"
    USERS ||--o{ TRANSACTIONS : "makes"



```

## Normalization of Tables

**Normalization:**

Normalization is a method of organizing data within table in a manner that minimizes redundancy and maintains data integrity.

- **1NF (First Normal Form):** Ensures that all columns are atomic (ie: no multiple values in a single column) and each column contains unique and indivisible data.

- **2NF (Second Normal Form):** Removes partial dependencies. This ensuring that non-key attributes depend on the entire composite primary key, not just part of it. Tables must first be in 1NF.

- **3NF (Third Normal Form):** Removes transitive dependencies, ensuring that non-key attributes depend only on the primary key and not on other non-key attributes. Tables must first be in 2NF.

- **4NF (Fourth Normal Form):** Ensures that tables are free from multi-valued dependencies. This can occur when one attribute in a table uniquely determines another set of attributes. 4NF ensures that if multiple independent relationships exist, they are separated into different tables. Tables must first be in 3NF.

All entities in this database model have been normalized to the third normal form (3NF), with minimal redundancy.

**Further Normalization of the MakeModelYear Table**

**Example of Higher Normalization (4NF):**

```mermaid
erDiagram
    CARS {
        car_id INT PK
        make_id INT FK
        model_id INT FK
        year_id INT FK
        mileage INT
        price FLOAT
        condition ENUM
        description VARCHAR(1000)
        image_url VARCHAR(100)
    }

    MAKE {
        make_id INT PK
        make_name VARCHAR(100)
    }

    MODEL {
        model_id INT PK
        model_name VARCHAR(100)
    }

    YEAR {
        year_id INT PK
        year INT
    }

    CARS }o--|| MAKE : "references"
    CARS }o--|| MODEL : "references"
    CARS }o--|| YEAR : "references"
```

The MakeModelYear table could have been further normalized to separate the make, model, and year into distinct tables as shown in the ERD above. In 4NF, the MakeModelYear table could be divided as follows:

**Make Table:** Contains distinct car manufacturers.
**Model Table:** Contains distinct car models.
**Year Table:** Stores car production years.

However, Due to the already complex nature of a two -sides marketplace and scope of this assignment, the choice was made to prioritize simplicity and performance over further normalization complexity.

**Benefits:**

- Further reduced redundancy in the MakeModelYear table.
- Improved data integrity by separating concerns into different tables.

**Drawbacks:**

- Increased complexity with multiple joins required to query for a car's make, model, and year.
- Higher overhead in managing three tables instead of one. Workload is increased.

## ORM Explanation

The ERD structue shown above has been implemented using the ORM (Object Relational Mapper) tool SQLAlchemy. Using an ORM such as this allows for more simplified code, removing the need for raw SQL queries by mapping database tables to Python classes. It also allows us to implement features such as query building, schemas, relationship management between tables.

**Key features used:**

- **Model Definitions:** Tables like User, Car, and Listing are defined as Python classes. The attributes are represented by columns.
- **Querying:** SQLAlchemy enables neat and easy querying, such as Car.query.all() to retrieve all cars or using filters like Listing.query.filter_by(listing_status='available')
- **Insertions and Updates:** New records are added via db.session.add() and saved with db.session.commit(), handling transactions efficiently.
- **Joins and Relationships:** SQLAlchemy handles relationships and joins with ease. It allowing us to access related data without complex SQL JOIN statements.
- **Schema Validation:** SQLAlchemy enforces column constraints like NOT NULL and UNIQUE, ensuring data integrity.

## Database System

We use PostgreSQL as the underlying database relationship management system for the the Car MARKETPLACE API. This system was chosen for its robustness, ACID compliance, and ability to handle complex queries efficiently. The API interacts with PostgreSQL through the ORM SQLAlchemy, which abstracts much of the complexity.

**Benefits of PostgreSQL:**

- **ACID Compliance:** Ensures data reliability and consistency.
- **Scalability:** PostgreSQL can handle the growing data needs of a the number of users, car, listings etc increases on the marketplace.
- **Complex Queries:** It supports advanced SQL features that allow for complex data retrieval, aggregation, and analysis.

**Drawbacks of PostgreSQL:**

- **Resource Consumption:** PostgreSQL is more resource heavy (e.g., CPU, memory) than lighter databases like SQLite.
- **Learning Curve:** The system's complexity can make it harder for beginners to learn and manage.

## Data Models (Entities)

### User Model

- **Table Name:** USERS
- **Description:** The `User` model stores information about users of the carmarketplace. This includes their email, password , and other personal details. This table has been normalized to 3NF.

- **Fields:**

  - `user_id` (INT, PK): Primary key, auto-incremented.
  - `name` (VARCHAR(100), NOT NULL): The user's full name.
  - `email` (VARCHAR(50), NOT NULL, UNIQUE): The user’s email, which must be unique.
  - `password_hash` (VARCHAR(255), NOT NULL): The hashed password for secure authentication.
  - `phone_number` (VARCHAR(15)): Optional phone number (can be null).
  - `address` (VARCHAR(255)): Optional address (can be null).

- **Cardinality & Relationships:**

  - **One-to-Many:** A user can create multiple listings (`LISTINGS`) and complete multiple transactions (`TRANSACTIONS`).
  - **Optional Relationships:**
    - A user may not create any listings; therefore, a user may exist without any related listings.
    - A user may not engage in any transactions; therefore, they can exist without any transactions

- **ORM Model:**

```python
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15))
    address = db.Column(db.String(255))

    # Relationships
    listings = db.relationship('Listing', back_populates='user')
    car_transactions = db.relationship('CarTransaction', back_populates='user')

    def __repr__(self):
        return f"<User {self.email}>"

```

- **Model Definitions:** Defines the User table, with attributes `user_id`, `name`, `email`, `password`, `phone_number`, and `address`.
- **Joins and Relationships:** This model relates to both the Listing and CarTransaction models, with a one-to-many relationship allowing a user to have multiple listings and transactions.

### Car Model

- **Table Name:** CARS
- **Description:** The `Car` model holds data about individual cars in the marketplace. The table stores attributes like mileage, price, and the car's condition. This table has been normalized to 3NF.

- **Fields:**

  - `car_id` (INT, PK): Primary key, auto-incremented.
  - `make_model_year_id` (INT, FK): Foreign key referencing the `MakeModelYear` table.
  - `mileage` (INT, NOT NULL): The mileage of the car in kilometers.
  - `price` (FLOAT, NOT NULL): The price of the car in the marketplace.
  - `condition` (ENUM('new', 'used', 'certified'), NOT NULL): The condition of the car.
  - `description` (VARCHAR(1000)): Optional description of the car (can be null).
  - `image_url` (VARCHAR(100)): Optional URL for the car’s image (can be null).

- **Cardinality & Relationships:**

  - **Many-to-One:** Each car references a specific make, model, and year via the `MakeModelYear` table.
  - **One-to-Many:** A car can be listed multiple times (`LISTINGS`) and sold multiple times (`TRANSACTIONS`).
  - **Optional Relationships:**
    - A car may not have any listings, meaning it has been added to the database but is not yet listed for sale.
    - A car may not have any transactions if it hasn't been sold.

- **ORM Model:**

```python
class Car(db.Model):
    __tablename__ = 'cars'

    car_id = db.Column(db.Integer, primary_key=True)
    make_model_year_id = db.Column(db.Integer, db.ForeignKey('makemodelyear.make_model_year_id'), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Enum('new', 'used', 'certified', name='car_condition_enum'), nullable=False)
    description = db.Column(db.String(1000))
    image_url = db.Column(db.String(100))

    # Relationships
    listings = db.relationship('Listing', back_populates='car')
    car_transactions = db.relationship('CarTransaction', back_populates='car')
    make_model_year = db.relationship('MakeModelYear', back_populates='cars')

    def __repr__(self):
        return f"<Car {self.car_id}, Price: {self.price}>"
```

- **Model Definitions:** Defines the Car table, with attributes `car_id`, `mileage`, `price`, `condition`, `description`, `image_url`, and `make_model_year_id`.

- **Joins and Relationships:** This model relates to the MakeModelYear, Listing, and CarTransaction models, with a many-to-one relationship to MakeModelYear and one-to-many relationships to both Listing and CarTransaction.

### Listing Model

- **Table Name:** LISTINGS
- **Description:** The `Listing` model represents a listing of a car in the marketplace. Each listing is associated with a car and a seller (user).

- **Fields:**

  - `listing_id` (INT, PK): Primary key, auto-incremented.
  - `car_id` (INT, FK): Foreign key referencing the `CARS` table.
  - `seller_id` (INT, FK): Foreign key referencing the `USERS` table.
  - `listing_status` (VARCHAR, NOT NULL): Status of the listing (e.g., available, sold).
  - `date_posted` (DATE, NOT NULL): The date the listing was posted.

- **Cardinality & Relationships:**

  - **Many-to-One:** A listing is associated with one car and one seller.
  - **Optional Relationships:**
    - A listing may not be linked to a transaction, meaning a car has been listed but hasn't been sold yet.

- **ORM Model:**

```python
class Listing(db.Model):
    __tablename__ = "listings"

    listing_id = db.Column(db.Integer, primary_key=True)
    listing_status = db.Column(
        db.Enum('available', 'sold', name='listing_status_enum'),
        nullable=False,
        default='available'
    )
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.car_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="listings")
    car = db.relationship("Car", back_populates="listings")

```

- **Model Definitions:** Defines the Listing table, with attributes `listing_id`, `listing_status`, `date_posted`,`car_id`,`user_id`.
- **Joins and Relationships:** This model relates to both the User and Car models, using foreign keys to reference those tables.

### CarTransaction Model

- **Table Name:** TRANSACTIONS
- **Description:** The `CarTransaction` model records the transactions of cars being sold on the marketplace. It stores information about the buyer, the car, the transaction date, and the sale price.

- **Fields:**

  - `transaction_id` (INT, PK): Primary key, auto-incremented.
  - `buyer_id` (INT, FK): Foreign key referencing the `USERS` table (the buyer).
  - `car_id` (INT, FK): Foreign key referencing the `CARS` table (the car sold).
  - `transaction_date` (DATE, NOT NULL): The date of the transaction.
  - `amount` (FLOAT, NOT NULL): The sale price of the car.

- **Cardinality & Relationships:**

  - **Many-to-One:** A transaction is associated with one buyer and one car.
  - **Optional Relationships:**
  - A car transaction must have both a buyer and a car, so there are no optional relationships here.

- **ORM Model:**

```python
class CarTransaction(db.Model):
    __tablename__ = "car_transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.car_id"), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    user = db.relationship("User", back_populates="car_transactions")
    car = db.relationship("Car", back_populates="car_transactions")

```

- **Model Definitions:** Defines the CarTransaction table, with attributes `transaction_id`, `transaction_date`, `amount`, `car_id`, and `buyer_id`.
- **Joins and Relationships:** This model relates to both the User and Car models, using foreign keys to reference those tables.

### MakeModelYear Model

- **Table Name:** MAKEMODELYEAR
- **Description:** The `MakeModelYear` model stores the make, model, and year of cars. This table could have been further normalized by separating these attributes into different tables, it was kept together to reduce complexity. This table is normalized to 2NF.

- **Fields:**

  - `make_model_year_id` (INT, PK): Primary key, auto-incremented.
  - `make` (VARCHAR(100), NOT NULL): The make of the car.
  - `model` (VARCHAR(100), NOT NULL): The model of the car.
  - `year` (INT, NOT NULL): The year the car was manufactured.

- **Cardinality & Relationships:**

  - **One-to-Many:** Each make, model, and year combination can be referenced by multiple cars in the `CARS` table.
  - **Optional Relationships:**
    - This relationship is not optional, as every car must have a valid make, model, and year reference

- **ORM Model:**

```python
class MakeModelYear(db.Model):
    __tablename__ = "makemodelyear"

    make_model_year_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    cars = db.relationship("Car", back_populates="make_model_year")

```

- **Model Definitions:** Defines the MakeModelYear table, with attributes `make_model_year_id`, `make`, `model`, and `year`.
- **Joins and Relationships:** This model relates to the Car model, with a one-to-many relationship, meaning multiple cars can reference a single make, model, and year combination.

---

# Local Setup & Developer Utilities

## Local Setup and Running Flask

**Setting Up the Environment**

Ensure that the environment is set up correctly by configuring your `.env` and `.flaskenv` files.

**Steps to Set Up:**

1. Create a .env file by copying the provided .env.example:

```bash
cp .env.example .env
```

2. Fill in the required values for DATABASE_URL and JWT_SECRET_KEY in the .env file:Example provided below.

```bash
DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/db_name"
JWT_SECRET_KEY="your_secret_key"
```

3. Ensure the .flaskenv file is set up correctly to configure Flask. Make sure flask_app redirects to `main.py`. If you want to run flask on debugging mode leave `FLASK_DEBUG=1` or else remove the line. You may choose any port you would like to run the flask application on. The default has been set to `8080`.

```bash
FLASK_APP=main
FLASK_DEBUG=1
FLASK_RUN_PORT=8080
```

4. source venv/bin/activate

```bash
source venv/bin/activate
```

5. Install project dependencies:

```bash
pip install -r requirements.txt
```

6. Run the Flask app:

```bash
flask run
```

With this, your Flask app will be up and running with all dependencies installed based on the configurations set in .env and .flaskenv.

## CLI Controllers

The Car Marketplace API includes several CLI (Command Line Interface) commands under the db_commands namespace to manage the database.
The command allow developers to interact and mange the database without the need to write raw SQL queries.

**Available CLI Commands**

The CLI commands are grouped under flask db_commands and allow developers to manage the database and seed data.

1. **Create Tables:**

- This creates all database tables as per the models.

```bash
flask db_commands create_tables
```

- If the models are working as expected, you should see the the message:

```bash
All tables created successfully!
```

- If an error occurs during table creation, you will receive a message like:

```bash
An error occurred while creating tables: <error message>
```

2. **Drop Tables:**

- This drops all the tables in the database,permanently deleting all data.

```bash
flask db_commands drop_tables
```

- After confirming, the following message will appear

```bash
All tables dropped successfully.
```

- If an error occurs while dropping tables, you will receive a message like:

```bash
An error occurred while dropping tables: <error message>
```

3. **Seed Database:** Seeds the database with initial data from a JSON file. Replace `<path/to/file>` with JSON file location.

```
flask db_commands seed <path/to/file>
```

- After seeding, the following message will appear:

```bash
Database seeded with data from the JSON file.
```

- If the specified file is not found, or if there is an error in reading the file or adding data:

```bash
File '<file_path>' not found.
Invalid JSON file format.
An error occurred: <error message>
```

- An example JSON file has been provided in the root directory of this project. It is called `seed_data.json`. To seed using this file:

```bash
flask db_commands seed_tables seed_data.json
```

- An example of the json file format has been provided below.

```json
{
  "users": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "password": "hashed_password_1",
      "phone_number": "1234567890",
      "address": "123 Main St",
      "is_admin": false
    },
    {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "password": "hashed_password_2",
      "phone_number": "0987654321",
      "address": "456 Elm St",
      "is_admin": true
    }
  ],
  "makemodelyears": [
    {
      "make": "Toyota",
      "model": "Corolla",
      "year": 2020
    },
    {
      "make": "Honda",
      "model": "Civic",
      "year": 2019
    }
  ],
  "cars": [
    {
      "make_model_year_id": 1,
      "mileage": 15000,
      "price": 20000,
      "condition": "used",
      "description": "Well-maintained sedan",
      "image_url": "http://example.com/car1.jpg"
    },
    {
      "make_model_year_id": 2,
      "mileage": 5000,
      "price": 22000,
      "condition": "new",
      "description": "Brand new model",
      "image_url": "http://example.com/car2.jpg"
    }
  ],
  "listings": [
    {
      "car_id": 1,
      "user_id": 1,
      "listing_status": "available",
      "date_posted": "2024-09-15"
    },
    {
      "car_id": 2,
      "user_id": 2,
      "listing_status": "sold",
      "date_posted": "2024-09-16"
    }
  ],
  "car_transactions": [
    {
      "car_id": 1,
      "buyer_id": 2,
      "transaction_date": "2024-09-20",
      "amount": 20000
    }
  ]
}
```

## PostgreSQL Setup

To set up and connect to PostgreSQL for local development:

1. **Install PostgreSQL:** Install PostgreSQL on your system if it isn't already present.

- **Ubuntu/Linux:**

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

- **macOS (using Homebrew):**

```bash
brew install postgresql
```

- **Windows:**
  - Download and install PostgreSQL from the [official site](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).

2. **Create a New Database:** After installing PostgreSQL, create a new database for the API:

```bash
sudo -u postgres psql
CREATE DATABASE car_market;
```

3. **Set Up Database Credentials:** Ensure your `.env` file contains the correct PostgreSQL credentials:

```bash
DATABASE_URL="postgresql+psycopg2://username:password@localhost:5432/car_market"
```

4. **Connect and Query the Database:** You can connect to PostgreSQL and query your database using psql

```bash
psql -U postgres -d car_market
```

5. **Use Cheatsheet:** You can now query the database using SQL commands. Commonly used commands can be found in the [SQL cheatsheet](https://www.sqltutorial.org/sql-cheat-sheet/)

---

# Error Handling & Status Codes

## Standard HTTP Status Codes

The Car Marketplace API uses several standard HTTP status codes. Belwo are some commonly used ones.

- **200 OK:** The request was successful. This is usually returned for successful GET, PUT, PATCH, or DELETE requests.
- **201 Created:** The resource has been successfully created. This is used for POST requests where a new record is created in the database.
- **400 Bad Request:** The server cannot process the request due to client error. This may be cause by equest syntax error or validation failure.
- **401 Unauthorized:** Returned when the user is not authenticated. Comminly returned if user's JWT token is missing or invalid.
- **403 Forbidden:** The is returned if the user does not have the necessary permissions to access the requested resource.
- **404 Not Found:** The requested resource was not found in the system.
- **500 Internal Server Error:** This is a generic error when something unexpected happens on the server.

## Custom Error Messages for Developer Debugging

**Authorization Controller (auth_controller.py)**

- **Error**: `{"error": "User does not exist."}`
  - Occurs when trying to fetch or update a user that does not exist.
- **Error**: `{"error": "Invalid email or password."}`
  - Returned during login when incorrect credentials are provided.
- **Error**: `{"error": "Email address must be unique."}`
  - Raised when attempting to register a user with a duplicate email.
- **Error**: `{"error": "You do not have permission to update this user's information."}`
  - Occurs when a non-admin user tries to update another user’s info.

**Car Controller (car_controller.py)**

- **Error**: `{"error": "Invalid make_model_year_id."}`
  - Occurs when referencing an invalid `make_model_year_id` in a request.
- **Error**: `{"error": "Car not found."}`
  - Raised when a car with the specified `car_id` does not exist.
- **Error**: `{"error": "You do not have permission to perform this action."}`
  - Occurs when a non-admin user tries to perform an admin-restricted action.

**Listing Controller (listing_controller.py)**

- **Error**: `{"error": "Listing not found."}`
  - Raised when attempting to access or update a listing that does not exist.
- **Error**: `{"error": "This car is already listed."}`
  - Occurs when a car is already listed, preventing duplicate listings.
- **Error**: `{"error": "Unauthorized access."}`
  - Raised when a user without permission tries to update or delete a listing.
- **Error**: `{"error": "Invalid listing status."}`
  - Occurs when the listing status (e.g., "sold", "available") is invalid.

**Car Transaction Controller (car_transaction_controller.py)**

- **Error**: `{"error": "Invalid car_id."}`
  - Raised when the car ID provided is invalid or does not exist.
- **Error**: `{"error": "User not found."}`
  - Occurs when referencing a non-existent buyer during a transaction.
- **Error**: `{"error": "'{field}' is required."}`
  - Raised when required fields such as `car_id` or `amount` are missing.
- **Error**: `{"error": "Car is not available for purchase."}`
  - Occurs when attempting to purchase a car that is no longer available (e.g., already sold).
- **Error**: `{"error": "Amount does not match car price."}`
  - Raised when the transaction amount does not match the listed price of the car.

**MakeModelYear Controller (makemodelyear_controller.py)**

- **Error**: `{"error": "This make, model, and year combination already exists."}`
  - Occurs when trying to create a duplicate make-model-year combination.
- **Error**: `{"error": "MakeModelYear not found."}`
  - Raised when attempting to reference or update a non-existent make-model-year combination.
- **Error**: `{"error": "Cannot delete MakeModelYear with associated cars. Delete associated cars first."}`
  - Occurs when trying to delete a MakeModelYear entry that is linked to cars.

**Models (Errors related to constraints)**

- **Unique constraints**:
  - `"error": "Email address must be unique"` (User model - when creating or updating a user).
- **Not-null constraints**:
  - `"error": "The column {column_name} is required"` (applies to various models like `Car`, `User`, etc.).

---

# Security

## JWT Token Security

As explained in the former section [Authentication & Authorization](#authentication--authorization). The Car Marketplace API uses JWT (JSON Web Tokens) for secure user authentication and authorization. Upon login, a JWT token is generated, and it must be included in the `Authorization` header for all subsequent requests.

**Token Expiry**

The default JWT expiration time limit for this API is set to **1 day**. The token is set to expire after 24 hours. After which, the user will need to log in again to receive a new token.

**Note for Developers**

This expiration limit is handled within the `auth_controller.py` file using the `create_access_token` function from the `flask_jwt_extended` library.

```python
from flask_jwt_extended import create_access_token
from datetime import timedelta

# Generating JWT token with 1-day expiration
token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
```

The token expiration can be adjusted by changing the value of `timedelta` in the auth_controller.py file. For example:

- To set the token expiration to 12 hours:

```python
token = create_access_token(identity=user.id, expires_delta=timedelta(hours=12))
```

- To set the token expiration to 7 days:

```python
token = create_access_token(identity=user.id, expires_delta=timedelta(hours=12))
```

**Token Validation**

For protected endpoints, the JWt token must be included in the `header` of the request under `Authorization`. If the token is missing, expired, or invalid, a `401 Unauthorized` error is returned.

In `Insomnia`, he token should be passed like this:

1. Open Insomnia and select the protected endpoint you want to test.
2. In the request, go to the Headers tab.
3. Add a new header with the following key-value pair:

- Key: `Authorization`
- Value: `Bearer <Your JWT Token>`

For example, if your token is eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..., your header will look like:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

4. After adding the token, click Send to make the request.

## Best Practices for Securing API Keys

Securing API keys and sensitive information like JWT secret keys and database credentials is crucial for the overall security of any application, including the Car Marketplace API. Please follow these best practices provided below:

1. **Store API Keys in Environment Variables**

- Sensitive Information like the JWT secret key should not be hard-coded in the source code of the API. Please use the `.envexample` to create your own `.env` file. A `gitignore` file that excludes the `.env` file from being added to the git repository is already present in the root directory.

2. **Limit Access to Secrets**

- Ensure that the `.env` is only accessed by trusted individuals. Limit read/write access to these files.

3. **Rotate API Keys Regularly**

- Regularly change your API key, JWT secret keys, and other credentials. This can help mitigate risk of security begin compromised.

4. **Use Secure Connections**

- Always serve your API over HTTPS to ensure that any sensitive data, such as tokens or API keys, are transmitted securely over the network.

5. **Avoid Logging Sensitive Information**

- Ensure sensitive information such as API keys, JWT tokens, or personal user information is excluded from logs.

6. **Use Strong Secret Keys**

- Use complicated combinations for your JWT secret key. strong secret key should be long, random, and hard to guess.
- Example of a strong JWT secret key:

```bash
JWT_SECRET_KEY = "a_random_very_long_string_with_special_characters"
```

7. **Set Proper Access Control**

- Implement proper access control that limits the permission based on user roles. Admin access should be restricted, and sensitive endpoints should be protected.

---

# Testing

## Testing Procedure

#### Test Planning and Design

To begin testing, we started off by identifying a comprehensive list of cases that would cover both normal operations and edge cases. The details of the each test can be found in the tables below.

\*Please note that the tables must already be created and seeded in PostgreSQL. To do that see section [CLI Controllers](#cli-controllers).

#### Testing Tables

**Users/Authentication Endpoints**

| **Endpoint**                | **Test Type**            | **Test Description**                                           | **Expected Outcome**                                  | **Patch Required?** | **Patch Commit Hash** |
| --------------------------- | ------------------------ | -------------------------------------------------------------- | ----------------------------------------------------- | ------------------- | --------------------- |
| **POST** `/api/register`    | Valid Registration       | Register a new user with valid data.                           | **201 Created**, user is successfully registered.     | No                  | N/A                   |
| **POST** `/api/register`    | Missing Required Fields  | Attempt to register without required fields (email, password). | **400 Bad Request**, error indicating missing fields. | No                  | N/A                   |
| **POST** `/api/register`    | Invalid Email Format     | Register with an invalid email format.                         | **400 Bad Request**, "Invalid Email Format."          | No                  | N/A                   |
| **POST** `/api/register`    | Duplicate Email          | Attempt to register with an email that already exists.         | **400 Bad Request**, "Email address must be unique."  | No                  | N/A                   |
| **POST** `/api/register`    | Password Not Provided    | Register without providing a password.                         | **400 Bad Request**, "Password is required."          | No                  | N/A                   |
| **POST** `/api/login`       | Valid Login              | Log in with valid credentials.                                 | **200 OK**, JWT token is returned.                    | No                  | N/A                   |
| **POST** `/api/login`       | Invalid Password         | Log in with incorrect password.                                | **400 Bad Request**, "Invalid email or password."     | No                  | N/A                   |
| **POST** `/api/login`       | Non-existent Email       | Log in with an email that doesn't exist.                       | **400 Bad Request**, "Invalid email or password."     | No                  | N/A                   |
| **PUT** `/api/users/:id`    | Valid Update by Self     | User updates their own information.                            | **200 OK**, updated user data is returned.            | No                  | N/A                   |
| **PUT** `/api/users/:id`    | Valid Update by Admin    | Admin updates another user's information.                      | **200 OK**, updated user data is returned.            | No                  | N/A                   |
| **PUT** `/api/users/:id`    | Unauthorized Update      | User tries to update another user's info without admin rights. | **403 Forbidden**, "You do not have permission..."    | No                  | N/A                   |
| **PUT** `/api/users/:id`    | Update Non-existent User | Attempt to update a user that doesn't exist.                   | **404 Not Found**, "User does not exist."             | No                  | N/A                   |
| **PUT** `/api/users/:id`    | Invalid Data Update      | Provide invalid data when updating user (e.g., invalid email). | **400 Bad Request**, "Invalid Email Format."          | No                  | N/A                   |
| **DELETE** `/api/users/:id` | Valid Delete by Admin    | Admin deletes a user.                                          | **200 OK**, "User deleted successfully."              | No                  | N/A                   |
| **DELETE** `/api/users/:id` | Unauthorized Delete      | Non-admin user attempts to delete a user.                      | **403 Forbidden**, "You do not have permission..."    | No                  | N/A                   |
| **DELETE** `/api/users/:id` | Delete Non-existent User | Attempt to delete a user that isn't in the database.           | **404 Not Found**, "User does not exist."             | No                  | N/A                   |

**Car Endpoints**

| **Endpoint**               | **Test Type**                | **Test Description**                                                     | **Expected Outcome**                                                    | **Patch Required?** | **Patch Commit Hash** |
| -------------------------- | ---------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------- | ------------------- | --------------------- |
| **GET** `/api/cars`        | Retrieve All Cars            | Fetch all cars in the database.                                          | **200 OK**, list of all cars is returned.                               | No                  | N/A                   |
| **GET** `/api/cars/:id`    | Valid Car ID                 | Retrieve a specific car by valid ID.                                     | **200 OK**, car data is returned.                                       | No                  | N/A                   |
| **GET** `/api/cars/:id`    | Non-existent Car ID          | Attempt to retrieve a car with an ID that doesn't exist.                 | **404 Not Found**, "Car not found."                                     | No                  | N/A                   |
| **POST** `/api/cars`       | Valid Creation by Admin      | Admin creates a new car with valid data.                                 | **201 Created**, car is successfully added.                             | No                  | N/A                   |
| **POST** `/api/cars`       | Unauthorized Creation        | Non-admin user attempts to create a new car.                             | **403 Forbidden**, "You do not have permission to perform this action." | No                  | N/A                   |
| **POST** `/api/cars`       | Missing Required Fields      | Omit required fields (e.g., `mileage`, `price`, `condition`).            | **400 Bad Request**, validation error messages are returned.            | No                  | N/A                   |
| **POST** `/api/cars`       | Invalid `make_model_year_id` | Use a `make_model_year_id` that doesn't exist.                           | **400 Bad Request**, "Invalid make_model_year_id."                      | No                  | N/A                   |
| **POST** `/api/cars`       | Invalid Condition Value      | Provide an invalid `condition` value (not 'new', 'used', 'certified').   | **400 Bad Request**, validation error on `condition`.                   | No                  | N/A                   |
| **PUT** `/api/cars/:id`    | Valid Update by Admin        | Admin updates an existing car with valid data.                           | **200 OK**, updated car data is returned.                               | No                  | N/A                   |
| **PUT** `/api/cars/:id`    | Unauthorized Update          | Non-admin user attempts to update a car.                                 | **403 Forbidden**, "You do not have permission to perform this action." | No                  | N/A                   |
| **PUT** `/api/cars/:id`    | Update Non-existent Car      | Attempt to update a car that doesn't exist.                              | **404 Not Found**, "Car not found."                                     | No                  | N/A                   |
| **PUT** `/api/cars/:id`    | Invalid Data Update          | Provide invalid data during update (e.g., invalid `make_model_year_id`). | **400 Bad Request**, validation error messages are returned.            | No                  | N/A                   |
| **DELETE** `/api/cars/:id` | Valid Delete by Admin        | Admin deletes a car with no associated transactions.                     | **200 OK**, "Car deleted successfully."                                 | No                  | N/A                   |
| **DELETE** `/api/cars/:id` | Unauthorized Delete          | Non-admin user attempts to delete a car.                                 | **403 Forbidden**, "You do not have permission to perform this action." | No                  | N/A                   |
| **DELETE** `/api/cars/:id` | Delete Non-existent Car      | Attempt to delete a car that doesn't exist.                              | **404 Not Found**, "Car not found."                                     | No                  | N/A                   |
| **DELETE** `/api/cars/:id` | Delete Car with Transactions | Attempt to delete a car that has associated transactions.                | **400 Bad Request**, error about associated transactions.               | No                  | N/A                   |

**Car Transaction Endpoints**

| **Endpoint**                        | **Test Type**               | **Test Description**                                                      | **Expected Outcome**                                                 | **Patch Required?** | **Patch Commit Hash** |
| ----------------------------------- | --------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------- | --------------------- |
| **GET** `/api/car-transactions`     | Valid Request               | Retrieve all car transactions with a valid JWT token.                     | **200 OK**, list of all transactions is returned.                    | No                  | N/A                   |
| **GET** `/api/car-transactions`     | Unauthorized Request        | Attempt to retrieve transactions without a JWT token.                     | **401 Unauthorized**, error about missing or invalid authentication. | No                  | N/A                   |
| **GET** `/api/car-transactions/:id` | Valid Transaction ID        | Retrieve a specific transaction by valid ID with JWT.                     | **200 OK**, transaction data is returned.                            | No                  | N/A                   |
| **GET** `/api/car-transactions/:id` | Non-existent Transaction ID | Attempt to retrieve a transaction with an ID that doesn't exist.          | **404 Not Found**, "Car transaction not found."                      | No                  | N/A                   |
| **GET** `/api/car-transactions/:id` | Unauthorized Request        | Attempt to retrieve a transaction without a JWT token.                    | **401 Unauthorized**, error about missing or invalid authentication. | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Valid Purchase              | Create a new transaction with valid data and JWT.                         | **201 Created**, transaction is successfully created.                | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Unauthorized Request        | Attempt to create a transaction without a JWT token.                      | **401 Unauthorized**, error about missing or invalid authentication. | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Missing Required Fields     | Omit required fields like `car_id` or `amount`.                           | **400 Bad Request**, error indicating missing fields.                | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Invalid `car_id`            | Use a `car_id` that doesn't exist.                                        | **400 Bad Request**, "Invalid car_id."                               | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Car Not Available           | Attempt to purchase a car that is not available (no 'available' listing). | **400 Bad Request**, "Car is not available for purchase."            | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Amount Mismatch             | Provide an `amount` that doesn't match the car's price.                   | **400 Bad Request**, "Amount does not match car price."              | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Purchase Already Sold Car   | Attempt to purchase a car that has already been sold.                     | **400 Bad Request**, "Car is not available for purchase."            | No                  | N/A                   |
| **POST** `/api/car-transactions`    | Invalid Amount Value        | Provide an invalid `amount` (e.g., negative number).                      | **400 Bad Request**, validation error messages.                      | No                  | N/A                   |

**Make Model Year Endpoints**

| **Endpoint**                        | **Test Type**             | **Test Description**                                        | **Expected Outcome**                                                          | **Patch Required?** | **Patch Commit Hash** |
| ----------------------------------- | ------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------- | --------------------- |
| **GET** `/api/makemodelyear`        | Valid Request             | Retrieve all make, model, year combinations.                | **200 OK**, list of all entries is returned.                                  | No                  | N/A                   |
| **GET** `/api/makemodelyear/:id`    | Valid ID                  | Retrieve a specific entry by valid ID.                      | **200 OK**, entry data is returned.                                           | No                  | N/A                   |
| **GET** `/api/makemodelyear/:id`    | Non-existent ID           | Attempt to retrieve an entry with an ID that doesn't exist. | **404 Not Found**, "MakeModelYear not found."                                 | No                  | N/A                   |
| **POST** `/api/makemodelyear`       | Valid Creation by Admin   | Admin creates a new entry with valid data.                  | **201 Created**, entry is successfully added.                                 | No                  | N/A                   |
| **POST** `/api/makemodelyear`       | Unauthorized Creation     | Non-admin user attempts to create a new entry.              | **403 Forbidden**, "You do not have permission to perform this action."       | No                  | N/A                   |
| **POST** `/api/makemodelyear`       | Missing Required Fields   | Omit required fields (e.g., `make`, `model`, `year`).       | **400 Bad Request**, validation error messages are returned.                  | No                  | N/A                   |
| **POST** `/api/makemodelyear`       | Duplicate Entry           | Attempt to create an entry that already exists.             | **400 Bad Request**, "This make, model, and year combination already exists." | No                  | N/A                   |
| **POST** `/api/makemodelyear`       | Invalid Data              | Provide invalid data (e.g., non-integer `year`).            | **400 Bad Request**, validation error messages are returned.                  | No                  | N/A                   |
| **PUT** `/api/makemodelyear/:id`    | Valid Update by Admin     | Admin updates an existing entry with valid data.            | **200 OK**, updated entry data is returned.                                   | No                  | N/A                   |
| **PUT** `/api/makemodelyear/:id`    | Unauthorized Update       | Non-admin user attempts to update an entry.                 | **403 Forbidden**, "You do not have permission to perform this action."       | No                  | N/A                   |
| **PUT** `/api/makemodelyear/:id`    | Update Non-existent Entry | Attempt to update an entry that doesn't exist.              | **404 Not Found**, "MakeModelYear not found."                                 | No                  | N/A                   |
| **PUT** `/api/makemodelyear/:id`    | Invalid Data Update       | Provide invalid data during update (e.g., invalid `year`).  | **400 Bad Request**, validation error messages are returned.                  | No                  | N/A                   |
| **DELETE** `/api/makemodelyear/:id` | Valid Delete by Admin     | Admin deletes an entry with no associated cars.             | **200 OK**, "MakeModelYear deleted successfully."                             | No                  | N/A                   |
| **DELETE** `/api/makemodelyear/:id` | Unauthorized Delete       | Non-admin user attempts to delete an entry.                 | **403 Forbidden**, "You do not have permission to perform this action."       | No                  | N/A                   |
| **DELETE** `/api/makemodelyear/:id` | Delete Non-existent Entry | Attempt to delete an entry that doesn't exist.              | **404 Not Found**, "MakeModelYear not found."                                 | No                  | N/A                   |
| **DELETE** `/api/makemodelyear/:id` | Delete Entry with Cars    | Attempt to delete an entry that has associated cars.        | **400 Bad Request**, error about associated cars.                             | No                  | N/A                   |

**Listing Endpoints**

| **Endpoint**                   | **Test Type**               | **Test Description**                                                 | **Expected Outcome**                                                 | **Patch Required?** | **Patch Commit Hash** |
| ------------------------------ | --------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------- | --------------------- |
| **GET** `/api/listings`        | Valid Request               | Retrieve all listings.                                               | **200 OK**, list of all listings is returned.                        | No                  | N/A                   |
| **GET** `/api/listings/:id`    | Valid Listing ID            | Retrieve a specific listing by valid ID.                             | **200 OK**, listing data is returned.                                | No                  | N/A                   |
| **GET** `/api/listings/:id`    | Non-existent Listing ID     | Attempt to retrieve a listing with an ID that doesn't exist.         | **404 Not Found**, "Listing not found."                              | No                  | N/A                   |
| **POST** `/api/listings`       | Valid Creation              | Authenticated user creates a new listing with valid data.            | **201 Created**, listing is successfully added.                      | No                  | N/A                   |
| **POST** `/api/listings`       | Unauthorized Creation       | Attempt to create a listing without a JWT token.                     | **401 Unauthorized**, error about missing or invalid authentication. | No                  | N/A                   |
| **POST** `/api/listings`       | Missing Required Fields     | Omit required fields (e.g., `car_id`).                               | **400 Bad Request**, validation error messages are returned.         | No                  | N/A                   |
| **POST** `/api/listings`       | Invalid `car_id`            | Use a `car_id` that doesn't exist.                                   | **400 Bad Request**, "Invalid car_id."                               | No                  | N/A                   |
| **POST** `/api/listings`       | Car Already Listed          | Attempt to list a car that is already listed.                        | **400 Bad Request**, "This car is already listed."                   | No                  | N/A                   |
| **PUT** `/api/listings/:id`    | Valid Update by Owner       | Owner updates their listing with valid data.                         | **200 OK**, updated listing data is returned.                        | No                  | N/A                   |
| **PUT** `/api/listings/:id`    | Valid Update by Admin       | Admin updates a listing with valid data.                             | **200 OK**, updated listing data is returned.                        | No                  | N/A                   |
| **PUT** `/api/listings/:id`    | Unauthorized Update         | Non-owner, non-admin user attempts to update a listing.              | **403 Forbidden**, "Unauthorized access."                            | No                  | N/A                   |
| **PUT** `/api/listings/:id`    | Update Non-existent Listing | Attempt to update a listing that doesn't exist.                      | **404 Not Found**, "Listing not found."                              | No                  | N/A                   |
| **PUT** `/api/listings/:id`    | Invalid Data Update         | Provide invalid data during update (e.g., invalid `listing_status`). | **400 Bad Request**, "Invalid listing status."                       | No                  | N/A                   |
| **DELETE** `/api/listings/:id` | Valid Delete by Owner       | Owner deletes their own listing.                                     | **200 OK**, "Listing deleted successfully."                          | No                  | N/A                   |
| **DELETE** `/api/listings/:id` | Valid Delete by Admin       | Admin deletes a listing.                                             | **200 OK**, "Listing deleted successfully."                          | No                  | N/A                   |
| **DELETE** `/api/listings/:id` | Unauthorized Delete         | Non-owner, non-admin user attempts to delete a listing.              | **403 Forbidden**, "Unauthorized access."                            | No                  | N/A                   |
| **DELETE** `/api/listings/:id` | Delete Non-existent Listing | Attempt to delete a listing that doesn't exist.                      | **404 Not Found**, "Listing not found."                              | No                  | N/A                   |

#### Implementing Tests in Insomnia

**Creating a JSON Import File**

To streamline the testing process in, a JSON file was created that could be used to easily import requests into Insomnia.

- The file can be found in the `Testing` folder under the name `insomnia_import.json`
- The test requests have been organized into logical groups that correspond to each endpoint category.
- The JSON file Includes URLs, methods, headers, and body content where applicable.
- Variables have been used in the JSON file such as `{{access_token}}` and `{{user_id}}`. These types of variables have to be replaced with actual values during testing. Alternatively you can also use the `environment variables` in Insomnia as outlined below.

**Using Environment Variables**

To enhance testing flexibility, we utilized environmental variables that have to be manually added to Insomnia.

- The `environment variables` allows us to quickly change variables in requests.
- These variables need to be added to Insomnia in the section `Manage Environments`
- A template file `environment_template.json` is provided in the `Testing` folder. You would have to fill in the variables by yourself.
- Instructions for Filling Variables:

  - **Obtain Access Tokens:**
    - **Regular User** `(access_token)`:
      1. Use the Login request to authenticate as the user with user_id.
      2. Copy the JWT token from the response body.
      3. Paste it into the access_token variable.
    - **Admin User** `(admin_access_token)`:
      1. Authenticate as the admin user (e.g., user_id 2).
      2. Copy the JWT token from the response.
      3. Paste it into the admin_access_token variable.
    - **Unauthorized User** `(unauthorized_access_token)`:
      1. Log in as another regular user (other_user_id).
      2. Copy the JWT token from the response.
      3. Paste it into the unauthorized_access_token variable.
  - **Set IDs:**
    - `user_id`: Set to the ID of the user you are authenticated as with `access_token` (e.g., "1").
    - `other_user_id`: Set to the ID of another user (e.g., "3").
    - `user_to_delete_id`: Set to the ID of the user you plan to delete in user deletion tests.
    - `car_id`: Use the ID of an existing car (e.g., "1").
    - `car_id_to_delete`: Use the ID of a car you intend to delete.
    - `car_id_with_transactions`: Use the ID of a car that has associated transactions.
    - `car_id_available`: Use the ID of a car that is available for purchase.
    - `car_id_sold`: Use the ID of a car that has already been sold.
    - `transaction_id`: Use the ID of an existing transaction.
    - `make_model_year_id`: Use the ID of an existing MakeModelYear entry.
    - `make_model_year_id_to_delete`: Use the ID of a MakeModelYear entry you intend to delete.
    - `make_model_year_id_with_cars`: Use the ID of a MakeModelYear that has associated cars.
    - `listing_id`: Use the ID of an existing listing.
    - `car_id_unlisted`: Use the ID of a car that is not yet listed.
    - `car_id_listed`: Use the ID of a car that is already listed.

- Finally, I have also included the actual environmental variables used in testing in a file called `environment_variables_used.json` in the same `Testing` folder. You would have to fill in `"access_token"`,`"admin_access_token"`,`"unauthorized_access_token"` as these tokens will not be same every time.

#### Running the Tests

Due to dependencies between requests, it's important to run tests in a specific order:

1. User Registration and Authentication:
2. MakeModelYear Endpoints:
3. Car Endpoints:
4. Listing Endpoints:
5. Car Transaction Endpoints:

#### Verifying Test Results

**Response Inspection:**

1. Check the response status codes.
2. Examine response bodies for expected data or error messages.
3. If expected result not seen, code patching is required.
4. Update [Testing Tables](#testing-tables) with patches and the respective git commit hash for record keeping.

# Project Management

## Project Timeline

## Sprint Planning & Milestones

### Epics and User Stories

### Task Breakdown and Assignments

## Jira/Project Management Tools Used

### Jira Boards and Tracking

#### Endpoint: `POST /api/register`

### Correct Request Testing:

1. **Description:** This endpoint registers a new user. Description [here](#user-endpoints)

2. **Request:**

   - **Method:** `GET/POST/PUT/DELETE/PATCH`
   - **URL:** `http://localhost:8080/api/<endpoint-path>`
   - **Headers:**
     ```json
     {
       "Authorization": "Bearer <JWT>",
       "Content-Type": "application/json"
     }
     ```
   - **Body (if applicable):**
     ```json
     {
       "<field1>": "<value1>",
       "<field2>": "<value2>"
     }
     ```

3. **Response:**

   - **Expected Response (200 OK):**
     ```json
     {
       "<response_field1>": "<response_value1>",
       "<response_field2>": "<response_value2>"
     }
     ```

4. **Example in Insomnia/Postman:**
   Include screenshot of the correct request and response (if possible).

---

### Breaking the Endpoint (Error Testing):

1. **Test 1: Missing Field(s):**

   - **Request:**
     ```json
     {
       "<field1>": "<value1>"
     }
     ```
   - **Expected Error Response (400 Bad Request):**
     ```json
     {
       "error": "<description_of_error>"
     }
     ```

2. **Test 2: Invalid JWT Token:**

   - **Request:**
     ```json
     {
       "Authorization": "Bearer <Invalid_JWT>"
     }
     ```
   - **Expected Error Response (401 Unauthorized):**
     ```json
     {
       "error": "Invalid or expired token"
     }
     ```

3. **Test 3: Invalid Input Data (if applicable):**

   - **Request:**
     ```json
     {
       "<field1>": "<invalid_value>"
     }
     ```
   - **Expected Error Response (422 Unprocessable Entity):**
     ```json
     {
       "error": "<specific_error_message>"
     }
     ```

4. **Other Possible Errors:**
   - Include any other test cases where the endpoint can break or return unexpected errors.

---

### Patching the Code (If Needed):

1. **Issue Found:**
   Describe the issue found in the initial testing.

2. **Patch Commit:**
   ```bash
   git commit -m "Fixed issue with <endpoint-path> [Commit Hash: xxxxxxxxxxxxx]"
   ```
