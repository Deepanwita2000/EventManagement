EventManagement

The main Django project configuration containing settings, URL configuration, ASGI, and WSGI configuration.

⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
cd EventManagement


Replace <your-repository-url> with your Git repository URL.

2. Create a virtual environment
Windows
python -m venv env
env\Scripts\activate

Linux / macOS
python3 -m venv env
source env/bin/activate

3. Install dependencies
pip install -r requirements.txt


If drf-spectacular is not present in your requirements file:

pip install drf-spectacular


Then update the requirements file:

pip freeze > requirements.txt

🔐 Environment Variables

Create a .env file in the root directory of the project.

Example:

DEBUG=True

SECRET_KEY=your-secret-key

DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret


Do not commit your .env file or API/payment credentials to GitHub.

Make sure .env is included in .gitignore.

🗄️ Database Setup

This project uses PostgreSQL.

Create a PostgreSQL database and configure the database credentials in .env.

Run migrations:

python manage.py makemigrations
python manage.py migrate


Create a superuser:

python manage.py createsuperuser

▶️ Running the Development Server

Start the Django development server:

python manage.py runserver


The API will normally be available at:

http://127.0.0.1:8000/

📚 API Documentation

The project uses drf-spectacular for automatic OpenAPI documentation.

After starting the server, the following endpoints are available.

Swagger UI
http://127.0.0.1:8000/api/docs/

ReDoc
http://127.0.0.1:8000/api/redoc/

OpenAPI Schema
http://127.0.0.1:8000/api/schema/


These endpoints are configured in:

path(
    "api/schema/",
    SpectacularAPIView.as_view(
        permission_classes=[AllowAny]
    ),
    name="schema"
),

path(
    "api/docs/",
    SpectacularSwaggerView.as_view(
        url_name="schema",
        permission_classes=[AllowAny]
    ),
    name="swagger-ui"
),

path(
    "api/redoc/",
    SpectacularRedocView.as_view(
        url_name="schema",
        permission_classes=[AllowAny]
    ),
    name="redoc"
),

🔗 API URL Structure

The project separates APIs into different applications.

Prefix	Application	Purpose
/event/	eventapp	Event-related APIs
/account/	accountapp	User/account APIs
/logic/	logicapp	Business logic APIs
/admin/	Django Admin	Administration
/api/docs/	drf-spectacular	Swagger documentation
/api/redoc/	drf-spectacular	ReDoc documentation
/api/schema/	drf-spectacular	OpenAPI schema

For example:

/event/...
/account/...
/logic/...


The exact endpoints under each prefix can be found in the corresponding application's urls.py.

🔑 Authentication

The project uses JWT-based authentication.

After successful login, the client should include the access token in authenticated requests.

Example:

Authorization: Bearer <access_token>


Example using cURL:

curl -X GET http://127.0.0.1:8000/account/profile/ \
     -H "Authorization: Bearer <access_token>"


The exact authentication endpoints depend on the implementation inside accountapp.

🔄 Celery & Redis

Celery is used for background/asynchronous tasks and Redis is used as the message broker.

Make sure Redis is running before starting Celery.

Start the Celery worker:

celery -A EventManagement worker --loglevel=info


On Windows, if required by your Celery setup:

celery -A EventManagement worker --loglevel=info --pool=solo


If Celery Beat is configured for scheduled tasks, start it with:

celery -A EventManagement beat --loglevel=info


For both worker and beat:

celery -A EventManagement worker --beat --loglevel=info


The exact Celery command may vary depending on your Celery configuration.

💳 Razorpay

The project includes Razorpay integration for payment processing.

Add your Razorpay credentials to .env:

RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret


Never expose your Razorpay secret key in frontend code or commit it to a public repository.

🖼️ Media & Static Files

Uploaded files are stored in the media/ directory.

Static assets are stored in the static/ directory.

During development, Django serves media files when:

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


Make sure your Django settings contain appropriate values for:

MEDIA_URL
MEDIA_ROOT
STATIC_URL
STATIC_ROOT

🧪 Running Tests

Run the Django test suite using:

python manage.py test


For a specific application:

python manage.py test eventapp

python manage.py test accountapp

python manage.py test logicapp

🧹 Useful Django Commands

Check the project for configuration issues:

python manage.py check


Create migrations:

python manage.py makemigrations


Apply migrations:

python manage.py migrate


Create an admin user:

python manage.py createsuperuser


Open the Django shell:

python manage.py shell


Collect static files:

python manage.py collectstatic

📦 Dependencies

The project dependencies are maintained in:

requirements.txt


Install them with:

pip install -r requirements.txt

🔒 Security Notes

Before deploying this project to production:

Set DEBUG=False
Use a strong Django SECRET_KEY
Store secrets in environment variables
Never commit .env
Configure ALLOWED_HOSTS
Configure CORS appropriately
Use HTTPS
Use secure database credentials
Protect Razorpay credentials
Configure secure JWT settings
Configure production static/media storage
Use a production-ready WSGI/ASGI server
Review Django security settings
🚀 Production

For production deployment, make sure to:

Configure PostgreSQL.
Configure Redis.
Configure environment variables.
Set DEBUG=False.
Configure ALLOWED_HOSTS.
Configure CORS.
Run database migrations.
Run collectstatic.
Start the application using a production server.
Start Celery workers separately.
Configure Celery Beat if scheduled tasks are required.
🤝 Contributing

Contributions are welcome.

Fork the repository.
Create a new branch.
git checkout -b feature/new-feature

Make your changes.
Run tests.
python manage.py test

Commit your changes.
git add .
git commit -m "Add new feature"

Push the branch.
git push origin feature/new-feature

Create a Pull Request.
📄 License

Add your project's license information here.

For example:

MIT License

👨‍💻 Author

Your Name

GitHub: <your-github-profile>

Email: <your-email>

⭐ Project Overview

This project provides a modular Django REST Framework backend for event management, user accounts, business logic, payments, and asynchronous background processing.

The API is organized into separate Django applications to keep the project maintainable and scalable.

For API exploration and testing, use the Swagger documentation:

http://127.0.0.1:8000/api/docs/





🧠 Logic App

The logicapp application contains the core business logic for ticket management, event bookings, seat availability, payment processing, and ticket generation.

It integrates with:

Django REST Framework
PostgreSQL
Razorpay
Celery
Redis
Email notifications

The base URL for these APIs is:

/logic/

🎟️ Ticket Management

Ticket management is handled through TicketViewSet.

Tickets can only be created, updated, or deleted by users with the organizer role.

Organizers can only manage tickets belonging to events that they created.

Create Ticket
Endpoint
POST /logic/tickets/

Authentication

Required.

Role

organizer

Request Body
{
    "name": "Early Bird",
    "event": 33,
    "price": "1000.00",
    "benefits": [
        "Middle seat",
        "Provide soft drinks"
    ],
    "available_seats": 250,
    "discount": "5.00",
    "tax": "18.00"
}

Validation Rules
Only organizers can create tickets.
The organizer must own the selected event.
Ticket names must be unique within an event.
A ticket cannot be created for another organizer's event.
Example Response
{
    "id": 10,
    "name": "Early Bird",
    "event": 33,
    "price": "1000.00",
    "benefits": [
        "Middle seat",
        "Provide soft drinks"
    ],
    "available_seats": 250,
    "discount": "5.00",
    "tax": "18.00"
}

✏️ Update Ticket
Endpoint
PUT /logic/tickets/<ticket_id>/


or:

PATCH /logic/tickets/<ticket_id>/

Authentication

Required.

Role

organizer

The organizer must be the owner of the ticket.

Success Response
{
    "message": "Ticket updated successfully.",
    "data": {
        "...": "updated ticket data"
    }
}

🗑️ Delete Ticket

Ticket deletion is implemented as a soft delete.

Instead of physically removing the ticket from the database, the ticket's is_active field is set to False.

Endpoint
DELETE /logic/tickets/<ticket_id>/

Authentication

Required.

Role

organizer

Success Response
{
    "message": "Ticket deleted successfully."
}

📖 Ticket Listing

The ticket queryset only returns active tickets:

Ticket.objects.filter(is_active=True)


Therefore, tickets that have been soft-deleted are not returned through the normal ticket listing endpoint.

🎫 Booking Tickets

Bookings are handled through BookingViewSet.

Only users with the user role can book tickets.

Endpoint
POST /logic/bookings/

Authentication

Required.

Role

user

Request Body
{
    "event_id": 33,
    "ticket_id": 10,
    "selected_seats": 2
}

Booking Validation

The following validations are performed:

Required fields

The following fields are mandatory:

event_id
ticket_id
selected_seats

Seat count

selected_seats must:

Be an integer
Be greater than zero
Not exceed the number of available seats
Event validation

The event must:

Exist
Be active
Ticket validation

The ticket must:

Exist
Be active
Belong to the selected event
Duplicate booking

A user cannot create another booking for the same event and ticket if they already have an existing booking.

💰 Booking Amount Calculation

The final booking amount is calculated using:

Base Amount
    ↓
Discount
    ↓
Subtotal
    ↓
Tax
    ↓
Final Amount

Formula
base_amount = ticket_price × selected_seats

discount_amount = base_amount × discount / 100

subtotal = base_amount - discount_amount

tax_amount = subtotal × tax / 100

final_amount = subtotal + tax_amount

Example

Suppose:

Ticket price = ₹1000
Seats = 2
Discount = 5%
Tax = 18%


Then:

Base amount = ₹1000 × 2
            = ₹2000

Discount = ₹2000 × 5%
         = ₹100

Subtotal = ₹2000 - ₹100
         = ₹1900

Tax = ₹1900 × 18%
    = ₹342

Final amount = ₹1900 + ₹342
             = ₹2242


The booking stores this calculated amount.

🔒 Atomic Booking Transaction

Booking creation uses:

with transaction.atomic():


This ensures that the booking operation and seat reduction are handled as a database transaction.

When a booking is successfully created:

Available seats
       ↓
Seats deducted
       ↓
Booking created
       ↓
Confirmation email task queued


If an error occurs during the transaction, the database changes are rolled back.

⏱️ Booking Expiration

When a booking is created, an expiration time is assigned:

expires_at = timezone.now() + timedelta(minutes=2)


Therefore, a newly created booking currently has a 2-minute expiration period.

This can be used together with Celery/background tasks to handle unpaid or expired reservations.

📧 Booking Confirmation Email

After a booking is created, a Celery task is queued:

send_booking_confirmation_email.delay(
    user.email,
    user.first_name,
    event.title,
    ticket.name,
    selected_seats,
    str(amount),
)


This means the email is handled asynchronously rather than blocking the API request.

The application therefore requires a running Celery worker for background email processing.

📋 User Bookings

Users can retrieve their own bookings.

Endpoint
GET /logic/bookings/

Authentication

Required.

The response contains booking information including:

Event
Ticket
Discount
Tax
Amount
Payment status
Example Response
{
    "data": [
        {
            "event": "Tech Conference 2026",
            "ticket": "Early Bird",
            "discount": "5.00",
            "tax": "18.00",
            "amount": "2242.00",
            "payment_status": "reserved"
        }
    ]
}


If the user has no bookings:

{
    "msg": "No bookings done!!"
}

💳 Razorpay Payment

The project integrates Razorpay for payment processing.

Razorpay credentials are loaded from environment variables:

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")


The Razorpay client is initialized using:

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

🧾 Create Payment Order

Payment processing is handled by MakePayment.

Endpoint
POST /logic/payment/

Authentication

Required.

Request Body
{
    "booking_id": 10
}


The booking must:

Exist
Belong to the authenticated user
Have a payment status of reserved
Razorpay Order Creation

The booking amount is converted from rupees to paise before being sent to Razorpay:

"amount": int(booking.amount * 100)


For example:

₹2242
   ↓
2242 × 100
   ↓
224200 paise


The Razorpay order uses:

Currency: INR
Receipt: Booking ID

Example Response
{
    "message": "Order created successfully.",
    "booking_id": 10,
    "order_id": "order_Q1AbCdEf12345",
    "amount": 224200,
    "currency": "INR"
}


The Razorpay order ID is stored against the booking.

🧪 Test Payment

The project currently contains a test payment-success function:

test_success(booking_id, user)


This simulates a successful Razorpay payment.

The booking is updated with:

payment_status = paid
razorpay_payment_id = pay_test_12345
razorpay_signature = signature_test


After payment is marked successful, ticket generation is triggered asynchronously:

generate_ticket.delay(booking.id)


The generated ticket can then be sent to the user's email.

Important: The current implementation is a test/simulation flow. In a production payment system, Razorpay's actual payment response and signature should be verified on the backend before marking a booking as paid.

🔄 Booking & Payment Flow

The overall process is:

User
 │
 │ 1. Select event
 ▼
Event
 │
 │ 2. Select ticket + seats
 ▼
Booking API
 │
 ├── Validate event
 ├── Validate ticket
 ├── Validate seats
 ├── Calculate discount
 ├── Calculate tax
 ├── Reduce available seats
 └── Create booking
 │
 ▼
Booking Status: reserved
 │
 │ 3. Create payment
 ▼
Razorpay
 │
 │ 4. Payment success
 ▼
Booking Status: paid
 │
 ▼
Celery
 │
 └── Generate ticket
       │
       ▼
     Email

👥 Role-Based Permissions

The logic application uses role-based access control.

Operation	User	Organizer
Book ticket	✅	❌
View own bookings	✅	Depends on implementation
Create ticket	❌	✅
Update ticket	❌	✅
Delete ticket	❌	✅
Manage another organizer's ticket	❌	❌
Organizer restrictions

An organizer can only manage tickets where:

ticket.created_by == request.user


Similarly, an organizer can only create tickets for events where:

event.created_by == request.user


This prevents one organizer from modifying another organizer's events or tickets.

🧵 Celery Background Tasks

The logic application uses Celery for asynchronous operations.

Currently, background tasks are used for:

Booking confirmation
send_booking_confirmation_email.delay(...)

Ticket generation
generate_ticket.delay(booking.id)


Make sure Redis and Celery are running when using these features.

Example:

celery -A EventManagement worker --loglevel=info


On Windows:

celery -A EventManagement worker --loglevel=info --pool=solo

🔐 Environment Variables

The logic application requires Razorpay credentials.

Add the following to .env:

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret


Never commit these values to Git.

⚠️ Important Implementation Notes
1. Payment security

The current MakePayment implementation calls:

msg = test_success(booking_id, user)


immediately after creating the Razorpay order.

This means the current implementation effectively simulates successful payment rather than waiting for the real Razorpay payment confirmation.

For production, the recommended flow is:

Create Razorpay Order
        ↓
Frontend opens Razorpay Checkout
        ↓
User completes payment
        ↓
Frontend receives Razorpay response
        ↓
Backend verifies Razorpay signature
        ↓
Mark booking as paid
        ↓
Generate ticket

2. Avoid printing secrets

The current implementation contains:

print(RAZORPAY_KEY_ID)
print(RAZORPAY_KEY_SECRET)


These should be removed before production deployment.

Never log:

RAZORPAY_KEY_SECRET


or other sensitive credentials.

3. Duplicate booking response

The duplicate booking check currently returns:

"already booked!"


It would be better for the API to return a consistent JSON response and an appropriate HTTP status such as 400 Bad Request or 409 Conflict.

Example:

{
    "message": "You have already booked this ticket for this event."
}

4. Payment amount

The API returns the Razorpay amount in paise:

224200


while the database booking amount is stored in rupees:

2242.00


This distinction should be documented clearly for frontend developers.

🧩 Logic App Responsibilities

In summary, logicapp is responsible for:

┌──────────────────────────────┐
│          logicapp            │
├──────────────────────────────┤
│                              │
│  🎟 Ticket Management        │
│                              │
│  🎫 Ticket Booking           │
│                              │
│  💰 Price Calculation        │
│     ├── Discount             │
│     └── Tax                  │
│                              │
│  💺 Seat Management          │
│                              │
│  💳 Razorpay Payments        │
│                              │
│  📧 Email Notifications      │
│                              │
│  🧾 Ticket Generation        │
│                              │
│  🔄 Celery Background Tasks  │
│                              │
└──────────────────────────────┘