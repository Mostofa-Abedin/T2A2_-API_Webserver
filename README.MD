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
  - [Summary of Endpoints](#summary-of-endpoints)
  - [Detailed Endpoints Reference](#detailed-endpoints-reference)
    - [User Endpoints](#user-endpoints)
    - [Car Endpoints](#car-endpoints)
    - [Listing Endpoints](#listing-endpoints)
    - [Car Transaction Endpoints](#car-transaction-endpoints)
- [Data Model](#data-model)
  - [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
  - [Data Models (Entities)](#data-models-entities)
    - [User Model](#user-model)
    - [Car Model](#car-model)
    - [Listing Model](#listing-model)
    - [CarTransaction Model](#cartransaction-model)
    - [MakeModelYear Model](#makemodelyear-model)
  - [Table Relationships](#table-relationships)
- [Developer Tools](#developer-tools)
  - [CLI Controllers](#cli-controllers)
  - [Admin Commands](#admin-commands)
- [Error Handling & Status Codes](#error-handling--status-codes)
  - [Standard HTTP Status Codes](#standard-http-status-codes)
  - [Custom Error Messages](#custom-error-messages)
  - [Sample Error Responses](#sample-error-responses)
- [Security](#security)
  - [JWT Token Security](#jwt-token-security)
  - [Best Practices for Securing API Keys](#best-practices-for-securing-api-keys)
- [Testing](#testing)
  - [Using Insomnia/Postman for Manual Testing](#using-insomniapostman-for-manual-testing)
- [Deployment](#deployment)
  - [Local Setup](#local-setup)
  - [Deployment Process](#deployment-process)
- [Project Management](#project-management)
  - [Project Timeline](#project-timeline)
  - [Sprint Planning & Milestones](#sprint-planning--milestones)
    - [Epics and User Stories](#epics-and-user-stories)
    - [Task Breakdown and Assignments](#task-breakdown-and-assignments)
  - [Jira/Project Management Tools Used](#jiraproject-management-tools-used)
    - [Jira Boards and Tracking](#jira-boards-and-tracking)
  - [Risk Management and Mitigation](#risk-management-and-mitigation)

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

# Endpoints

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

### Listing Endpoints

### Car Transaction Endpoints

# Data Model

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS {
        user_id INT PK
        name VARCHAR(100)
        email VARCHAR(50) UK
        password_hash VARCHAR(255)
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

    USERS ||--o{ LISTINGS : "creates"
    USERS ||--o{ TRANSACTIONS : "makes"

    CARS ||--o{ LISTINGS : "is listed in"
    CARS ||--o{ TRANSACTIONS : "is sold in"
    CARS }o--|| MAKEMODELYEAR : "references"

```

## Data Models (Entities)

### User Model

### Car Model

### Listing Model

### CarTransaction Model

### MakeModelYear Model

## Table Relationships

# Developer Tools

## CLI Controllers

## Admin Commands

# Error Handling & Status Codes

## Standard HTTP Status Codes

## Custom Error Messages

## Sample Error Responses

# Security

## JWT Token Security

## Best Practices for Securing API Keys

# Testing

## Using Insomnia/Postman for Manual Testing

# Deployment

## Local Setup

## Deployment Process

# Project Management

## Project Timeline

## Sprint Planning & Milestones

### Epics and User Stories

### Task Breakdown and Assignments

## Jira/Project Management Tools Used

### Jira Boards and Tracking

## Risk Management and Mitigation
