# FoodFeery

## Overview
FoodFeery is a food delivery website built using Django and Django REST Framework. Users can browse and order food from their favorite restaurants, while restaurant owners can manage their offerings and orders. Administrators have full control over the platform, managing users, restaurants, and food categories.

## Features

### User Functionality
- **User Authentication**: Login and logout capabilities.
- **Profile Management**: Users can update their profiles.
- **Order Food**: Users can view restaurants and order food.
- **Order History**: Users can view their previous orders.
- **Cart Management**: Add items to the cart, update quantities, or remove items.

### Restaurant Owner Functionality
- **Owner Authentication**: Login and logout for restaurant owners.
- **Manage Restaurant**: Owners can add, update, and delete restaurant information.
- **Menu Management**: Owners can add, update, and manage food items on their menus.
- **Order Management**: View and manage incoming orders.

### Admin Functionality
- **Admin Authentication**: Login and logout for admins.
- **User Management**: Admins can manage all users and modify their permissions.
- **Restaurant Management**: Create, update, and delete restaurant listings.
- **Category Management**: Admins can create and update food categories and subcategories.
- **Feedback Management**: Admins can view and manage user feedback.

## API Endpoints

### User Endpoints
- **POST /accounts/profile**: Update user profile.
- **POST /accounts/forget-password**: Request password reset.
- **POST /accounts/reset-password**: Reset user password.
- **GET /orders**: List all orders for the user.
- **GET /user-order-list**: Retrieve user's order history.
- **POST /add-to-cart/burger**: Add burger to cart.
- **POST /add-to-cart/pizza**: Add pizza to cart.
- **PATCH /update/cart-item/burger**: Update cart item for burger.
- **DELETE /delete/cart-item/burger**: Remove burger from cart.

### Restaurant Owner Endpoints
- **GET /restaurant/info/tripti-catering**: Get information about Tripti Catering restaurant.
- **PATCH /restaurant/update/tripti-catering**: Update Tripti Catering restaurant details.
- **DELETE /restaurant/delete/tripti-catering**: Delete Tripti Catering restaurant.

### Admin Endpoints
- **GET /admin/users**: List all users.
- **PATCH /admin/update-user/4/role/**: Update user role by ID.
- **POST /admin/users/change-permission**: Change user permissions.
- **PATCH /admin/restaurant/update/tripti-catering**: Update Tripti Catering restaurant details.
- **DELETE /admin/restaurant/delete/tripti-catering**: Delete Tripti Catering restaurant.
- **GET /admin/categories**: List all food categories.
- **PATCH /admin/categories/update/vegan**: Update vegan category.
- **DELETE /admin/categories/delete/vegan**: Delete vegan category.
- **GET /admin/category/items/details/vegan**: Get item details for vegan category.
- **POST /admin/tag/update/popular**: Update the "popular" tag.
- **DELETE /admin/tag/delete/popular**: Delete the "popular" tag.
- **GET /admin/tag-list**: List all tags (subcategories).
- **POST /admin/item/add**: Add a new food item.
- **PATCH /admin/item/update/burger**: Update burger details.
- **DELETE /admin/food/delete/burger**: Delete the burger item.
- **GET /admin/feedback/tripti-catering**: View feedback for Tripti Catering restaurant.
- **GET /admin/feedback-list/tripti-catering**: List all feedback for Tripti Catering restaurant.

### Category and Food Endpoints
- **GET /category-foods/pizza**: Get foods under the pizza category.
- **GET /info/tripti-catering**: Get Tripti Catering restaurant info.
- **GET /restaurant-food-list/tripti-catering**: List food items for Tripti Catering restaurant.
- **GET /tag-food-list/popular**: List food items associated with the "popular" tag.
- **GET /search-food/**: Search for food items.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/foodfeery.git
   cd foodfeery
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Feel free to submit issues and pull requests for enhancements or bug fixes!
