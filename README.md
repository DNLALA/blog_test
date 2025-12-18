# Django Blog API

A comprehensive blog API built with Django Rest Framework (DRF) for creating, managing, and interacting with blog posts and user profiles. This project includes user authentication, blog post creation, liking functionality, and commenting system.

## Tech Stack

- **Backend Framework**: Django 5.2.9
- **API Framework**: Django Rest Framework (DRF) 3.16.1
- **Authentication**: Simple JWT 5.5.1
- **Database**: PostgreSQL
- **API Documentation**: DRF Spectacular 0.29.0
- **Image Handling**: Pillow 12.0.0
- **Environment Management**: django-environ 0.12.0, python-dotenv 1.2.1
- **Deployment**: Docker, Gunicorn 23.0.0
- **Python Version**: 3.11

## Features

### User Management

- User registration with detailed profile information
- JWT-based authentication (login/logout)
- Custom user model with UUID primary keys
- Profile management including personal details, contact info, and profile photos

### Blog Functionality

- Create and publish blog posts with title, body, and cover photos
- Like/unlike blog posts
- Add comments to blog posts
- Retrieve lists of blog posts and comments with pagination
- Author attribution for posts and comments

### API Features

- RESTful API endpoints
- JWT authentication for protected endpoints
- Pagination for list views (10 items per page)
- Swagger UI for API documentation
- OpenAPI schema generation
- CORS support (configurable)
- Static and media file serving

## Project Structure

```
app/
├── app/                    # Main Django project
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── users/                  # User management app
│   ├── models.py          # User and UserProfile models
│   ├── api/
│   │   └── user_profile/
│   │       ├── serializers.py  # User serializers
│   │       ├── views.py       # Auth views
│   │       └── urls.py        # Auth URLs
│   └── migrations/        # Database migrations
├── blog/                   # Blog functionality app
│   ├── models.py          # BlogPost and Comment models
│   ├── api/
│   │   ├── serializers.py # Blog serializers
│   │   ├── views.py       # Blog views
│   │   └── urls.py        # Blog URLs
│   └── migrations/        # Database migrations
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker services configuration
├── manage.py              # Django management script
└── README.md              # This file
```

## Installation and Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11 (if running locally)

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

POSTGRES_DB=blog_db
POSTGRES_USER=blog_user
POSTGRES_PASSWORD=blog_password
POSTGRES_HOST=blog_db
POSTGRES_PORT=5432
```

### Running with Docker (Recommended)

1. Clone the repository and navigate to the app directory
2. Create the `.env` file as described above
3. Run the application:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8055`

### Running Locally

1. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the database (ensure PostgreSQL is running):

```bash
python manage.py migrate
```

4. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `POST /user_auth/register_user/` - Register a new user
- `POST /user_auth/login_user/` - Login user
- `POST /user_auth/logout_user/` - Logout user (requires authentication)

### Blog Posts

- `GET /blog/posts_list/` - List all blog posts (paginated)
- `POST /blog/blogpost-create/` - Create a new blog post (requires authentication)
- `POST /blog/blogpost-like/<int:pk>/` - Like/unlike a blog post (requires authentication)

### Comments

- `GET /blog/comments-list/` - List all comments (paginated)
- `POST /blog/comments-create/` - Create a new comment (requires authentication)

### API Documentation

- `GET /schema` - OpenAPI schema
- `GET /` - Swagger UI documentation
- `GET /admin/` - Django admin interface

## API Usage Examples

### User Registration

```json
POST /user_auth/register_user/
{
  "username": "johndoe",
  "password": "securepassword123",
  "profile": {
    "first_name": "John",
    "last_name": "Doe",
    "other_name": "Smith",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "gender": "Male",
    "date_of_birth": "1990-01-01",
    "address": "123 Main St, City, Country",
    "profile_photo": "base64-encoded-image-or-url"
  }
}
```

### User Login

```json
POST /user_auth/login_user/
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

Response includes JWT access and refresh tokens.

### Create Blog Post

```json
POST /blog/blogpost-create/
Authorization: Bearer <access_token>
{
  "title": "My First Blog Post",
  "body": "This is the content of my blog post...",
  "cover_photo": "image-file"
}
```

### Like a Blog Post

```json
POST /blog/blogpost-like/1/
Authorization: Bearer <access_token>
```

## Data Models

### User

- UUID primary key
- Username (unique)
- Password (hashed)
- User reference UID

### UserProfile

- One-to-one relationship with User
- Personal information: first_name, last_name, other_name
- Contact: email (unique), phone_number (unique)
- Demographics: gender, date_of_birth
- Address and profile_photo
- Timestamps: created_at, updated_at

### BlogPost

- Title and body content
- Cover photo (optional)
- Author (foreign key to UserProfile)
- Likes (many-to-many with UserProfile)
- Comments (related to Comment model)
- Timestamps: created_at, updated_at

### Comment

- Blog post reference
- Comment body
- Author (foreign key to UserProfile)
- Timestamp: created_at

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Access tokens expire after 60 minutes, refresh tokens after 1 day.

## Pagination

List endpoints return paginated results with 10 items per page. Use query parameters:

- `?page=1` - Specific page number
- `?page_size=20` - Custom page size

## File Uploads

The API supports image uploads for:

- User profile photos (stored in `staff/photos/`)
- Blog post cover photos (stored in `blog_covers/`)

Files are served via Django's media URL configuration.

## Testing

Run tests with:

```bash
python manage.py test
```

## Deployment

The application is containerized with Docker and can be deployed using the provided `docker-compose.yml`. For production:

1. Set `DEBUG=False` in environment variables
2. Configure proper secret keys
3. Set up proper database credentials
4. Configure static file serving (nginx, cloud storage, etc.)
5. Set up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
